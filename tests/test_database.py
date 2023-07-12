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

from datetime import datetime
from lethbridge.database import Base
from lethbridge.database import Faction
from lethbridge.database import System
from lethbridge.database import SystemSchema
from psycopg2cffi import compat
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

# invoke psycopg2cffi compatibility hook
compat.register()


def test_systemschema(mock_db_uri, mock_galaxy_dump):
    # initialize the database
    engine = create_engine(mock_db_uri, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    for load_data in mock_galaxy_dump:
        with Session.begin() as session:
            new_system = SystemSchema().load(load_data, session=session)
            session.add(new_system)

        with Session.begin() as session:
            new_system = session.get(System, load_data.get("id64"))
            dump_data = SystemSchema().dump(new_system)

        assert len(dump_data) <= len(load_data)
        for k in dump_data:
            if k == "powers":
                # not clear whether Spansh sorts this
                assert set(dump_data[k]) <= set(load_data[k])
            elif k == "stations":
                assert len(dump_data[k]) == len(load_data[k])
            elif k == "date":  # TODO
                pass
            else:
                assert dump_data[k] == load_data[k]

    with Session.begin() as session:
        fac = session.get(Faction, "Sol Workers' Party")
        assert len(fac.systems) == 4
