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

from copy import deepcopy
from datetime import datetime
from lethbridge.database import Base
from lethbridge.database import System
from lethbridge.database import SystemSchema
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
import pytest

test_data = {
    'id64': 0,
    'name': 'Test System A',
    'coords': {
        'x': 1.0,
        'y': 2.0,
        'z': 3.0,
    },
    'allegiance': None,
    'government': 'None',
    'primaryEconomy': 'None',
    'secondaryEconomy': 'None',
    'security': 'Anarchy',
    'population': 0,
    'bodyCount': 0,
    # controllingFaction
    # factions
    # powers
    'powerState': None,         # FIXME: omitted in dumps, presence
                                # demarcates the Bubble?
    'date': '1970-01-01T00:00:00',
    # bodies
    # stations
}


@pytest.fixture
def mock_database(tmp_path):
    mock_database_uri = 'sqlite:///' + str(tmp_path / 'lethbridge.sqlite')
    engine = create_engine(mock_database_uri)
    Base.metadata.create_all(engine)
    return engine


def test_system_schema(mock_database):
    with Session(mock_database) as session:
        test_system_prime = SystemSchema().load(
            deepcopy(test_data),
            session=session,
        )
        session.add(test_system_prime)
        session.commit()

        stmt = select(System).where(System.id64 == test_data.get('id64'))
        test_system_secunde = session.scalars(stmt).one()
        dump_data = SystemSchema().dump(test_system_secunde)

    assert test_system_prime == test_system_secunde
    assert len(test_data) == len(dump_data)
    for i in test_data:
        assert test_data[i] == dump_data[i]


def test_system_defaults(mock_database):
    with Session(mock_database) as session:
        test_system_prime = System(
            id64=test_data.get('id64'),
            name=test_data.get('name'),
            x=test_data.get('coords').get('x'),
            y=test_data.get('coords').get('y'),
            z=test_data.get('coords').get('z'),
            date=datetime.fromisoformat(test_data.get('date')),
        )
        session.add(test_system_prime)
        session.commit()
        dump_data = SystemSchema().dump(test_system_prime)

        stmt = select(System).where(System.id64 == test_data.get('id64'))
        test_system_secunde = session.scalars(stmt).one()

    assert test_system_prime == test_system_secunde
    assert len(test_data) == len(dump_data)
    for i in test_data:
        assert test_data[i] == dump_data[i]


# TODO: more things that should work
# TODO: things that should fail