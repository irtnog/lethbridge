# lethbridge, free/libre/open source client for EDDN (and more)
# Copyright (C) 2023  Matthew X. Economou
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.

from dateutil.parser import parse
from lethbridge.database import Base
from lethbridge.database import Faction
from lethbridge.database import System
from lethbridge.schemas.spansh import SystemSchema
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


def test_systemschema(mock_db_uri, mock_galaxy_dump):
    # initialize the database
    engine = create_engine(mock_db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    for load_data in mock_galaxy_dump:
        with Session.begin() as session:
            new_system = SystemSchema().load(load_data, session=session)
            session.add(new_system)

        with Session.begin() as session:
            new_system = session.get(System, load_data["id64"])
            dump_data = SystemSchema().dump(new_system)

        # compare keys; dump_data should be a subset of load_data
        # until we finish the System class
        assert set(dump_data) <= set(load_data)

        # compare values; some keys require special handling
        for k in dump_data:
            if k == "factions":
                d_fac = sorted(dump_data[k], key=lambda fac: fac["name"])
                l_fac = sorted(load_data[k], key=lambda fac: fac["name"])
                assert d_fac == l_fac

            elif k == "powers":
                assert set(dump_data[k]) == set(load_data[k])

            elif k == "bodies":
                # dump_data should have the same number of bodies
                assert len(dump_data[k]) == len(load_data[k])

                # # compare each body
                # for d_bd, l_bd in zip(
                #     sorted(dump_data[k], key=lambda bd: bd["bodyId"]),
                #     sorted(load_data[k], key=lambda bd: bd["bodyId"]),
                # ):
                #     # each dumped body should have a subset of the
                #     # corresponding loaded body's top-level keys (at
                #     # least until we finish implementing everything)
                #     assert set(d_bd) <= set(l_bd)

                #     # dumped bodies should have the same number of
                #     # surface ports and settlements (if any)
                #     if "stations" in l_bd:
                #         assert "stations" in d_bd
                #         assert len(d_bd["stations"]) == len(l_bd["stations"])

            elif k == "stations":
                # dump_data should have the same number of spaceports
                assert len(dump_data[k]) == len(load_data[k])

                # compare each station
                for d_st, l_st in zip(
                    sorted(dump_data[k], key=lambda st: st["name"]),
                    sorted(load_data[k], key=lambda st: st["name"]),
                ):
                    assert set(d_st) == set(l_st)

                    if "shipyard" in l_st:
                        assert "shipyard" in d_st

                        d_shipyard = d_st["shipyard"]
                        d_ships = d_shipyard["ships"]
                        l_shipyard = l_st["shipyard"]
                        l_ships = l_shipyard["ships"]
                        assert len(d_ships) == len(l_ships)

                        d_update_time = d_shipyard["updateTime"]
                        l_update_time = l_shipyard["updateTime"]
                        assert parse(d_update_time) == parse(l_update_time[:-3])

                    if "outfitting" in l_st:
                        assert "outfitting" in d_st

                        d_outfitting = d_st["outfitting"]
                        d_modules = d_outfitting["modules"]
                        l_outfitting = l_st["outfitting"]
                        l_modules = l_outfitting["modules"]
                        assert len(d_modules) == len(l_modules)

                        d_update_time = d_outfitting["updateTime"]
                        l_update_time = l_outfitting["updateTime"]
                        assert parse(d_update_time) == parse(l_update_time[:-3])

            elif k == "date":
                assert parse(dump_data[k]) == parse(load_data[k][:-3])

            else:
                assert dump_data[k] == load_data[k]

    # with the data loaded, make some queries
    with Session.begin() as session:
        stmt = select(func.count(System.id64))
        res = session.execute(stmt).first()
        assert res[0] == 9

        fac = session.get(Faction, "Sol Workers' Party")
        assert len(fac.systems) == 4
