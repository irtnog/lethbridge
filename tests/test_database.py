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
from lethbridge.database import State
from lethbridge.database import System
from lethbridge.database import SystemSchema
from psycopg2cffi import compat
from pytest import mark
from pytest import raises
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

# invoke psycopg2cffi compatibility hook
compat.register()


# Invoke smoke tests with `pytest -k smoke`.  See also
# https://docs.pytest.org/en/stable/mark.html,
# https://stackoverflow.com/a/52369721.
@mark.smoke
def test_orm_basic(mock_db_uri):
    engine = create_engine(mock_db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    with Session.begin() as session:
        new_system = System(
            id64=0,
            name="Test System",
            x=1.0,
            y=2.0,
            z=3.0,
            date=datetime(1970, 1, 1, 0, 0),
        )
        session.add(new_system)

        stmt = select(func.count(System.name))
        cnt = session.scalars(stmt).one()
        assert cnt == 1

    with raises(IntegrityError) as e_info:  # noqa: F841
        with Session.begin() as session:
            bad_system = System(
                id64=0,
                name="Bad System",
                x=1.0,
                y=2.0,
                z=3.0,
                date=datetime(1970, 1, 1, 0, 0),
            )
            session.add(bad_system)

    with Session.begin() as session:
        stmt = select(System).where(System.name.ilike("%test%"))
        existing_system = session.scalars(stmt).one()
        assert existing_system.name == "Test System"


@mark.smoke
def test_orm_relationships(mock_db_uri):
    engine = create_engine(mock_db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    with Session.begin() as session:
        bubble_faction = Faction(
            name="Bubble Faction",
            allegiance="Independent",
            government="Collective",
        )
        bubble_faction_state = State(
            faction=bubble_faction,
            influence=0.5,
            state="None",
        )
        bubble_system = System(
            id64=1,
            name="Bubble System",
            x=1.1,
            y=2.1,
            z=3.1,
            date=datetime(1970, 1, 1, 0, 1),
        )
        bubble_system.factions.append(bubble_faction_state)
        bubble_system.controllingFaction = bubble_faction
        session.add(bubble_system)

    with Session.begin() as session:
        stmt = select(Faction)
        rows = session.scalars(stmt).all()
        assert len(rows) == 1
        this_faction = rows[0]
        assert len(this_faction.controlledSystems) == 1
        assert len(this_faction.systems) == 1

        stmt = select(System).where(System.id64 == 1)
        this_system = session.scalars(stmt).one()
        assert this_system.controllingFaction == this_faction
        assert len(this_system.factions) == 1

        this_bgs_state = this_faction.systems[0]
        assert this_bgs_state.system == this_system


@mark.smoke
def test_systemschema_basic(mock_db_uri):
    engine = create_engine(mock_db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    with Session.begin() as session:
        another_system = System(
            id64=2,
            name="Another System",
            x=1.2,
            y=2.2,
            z=3.2,
            date=datetime(1970, 1, 1, 0, 2),
        )
        session.add(another_system)

    # Default values don't get set until commit time, but ending the
    # session (which automatically triggers a commit) breaks the ORM
    # object.  So get a new ORM object before proceeding.  (Using
    # sessionmaker sessions like this means session.commit() doesn't
    # work.  I don't know why.)
    with Session.begin() as session:
        another_system = session.get(System, 2)
        dump_data = SystemSchema().dump(another_system)
        assert "id64" in dump_data
        assert dump_data["name"] == "Another System"
        load_data = SystemSchema().load(dump_data, session=session)
        assert load_data == another_system
        session.delete(another_system)

    # The contents of dump_data shouldn't be mutated by
    # @post_dump/@pre_load methods of the relevant schemas, so it
    # should be fully reusable from session to session.
    with Session.begin() as session:
        deleted_system = session.get(System, 2)
        assert deleted_system is None
        restored_system = SystemSchema().load(dump_data, session=session)
        session.add(restored_system)

    with Session.begin() as session:
        checked_system = session.get(System, 2)
        assert checked_system is not None
        assert checked_system.name == "Another System"


def test_systemschema_real(mock_db_uri, mock_system_data):
    engine = create_engine(mock_db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    with Session.begin() as session:
        new_system = SystemSchema().load(mock_system_data, session=session)
        session.add(new_system)

    with Session.begin() as session:
        new_system = session.get(System, mock_system_data.get("id64"))
        dump_data = SystemSchema().dump(new_system)

    assert len(dump_data) <= len(mock_system_data)
    for k in dump_data:
        if k == "date":
            # TODO: Spansh's dumps do not use ISO 8601.  We do, and we
            # don't plan to be compatible with Spansh in this case.
            # Skip testing for now.  Parse and compare native datetime
            # types later.
            continue
        assert dump_data[k] == mock_system_data[k]
