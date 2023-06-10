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
from lethbridge.database import System
from lethbridge.database import SystemSchema
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
import pytest

test_data = {
    'id64': 0,
    'name': 'Test System A',
    # coords
    'allegiance': None,
    'government': None,
    'primaryEconomy': None,
    'secondaryEconomy': None,
    'security': None,
    'population': None,
    'bodyCount': None,
    # controllingFaction
    # factions
    # powers
    'powerState': None,
    'date': '1970-01-01T00:00:00',
    # bodies
    # stations
}


@pytest.fixture
def mock_database(tmp_path):
    mock_database_uri = 'sqlite:///' + str(tmp_path / 'lethbridge.sqlite')
    engine = create_engine(mock_database_uri)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        test_system_a = System(
            id64=0,
            name='Test System A',
            date=datetime(1970, 1, 1),
        )
        session.add(test_system_a)
        session.commit()
    return engine


def test_system_dump(mock_database):
    system_schema = SystemSchema()
    with Session(mock_database) as session:
        stmt = select(System).where(System.name == 'Test System A')
        system = session.scalars(stmt).one()
        dump_data = system_schema.dump(system)
    assert len(test_data) == len(dump_data)
    for i in test_data:
        assert test_data[i] == dump_data[i]


def test_system_load(mock_database):
    system_schema = SystemSchema()
    with Session(mock_database) as session:
        test_system_a_prime = system_schema.load(test_data, session=session)
    test_system_a_secunde = System(
        id64=0,
        name='Test System A',
        date=datetime(1970, 1, 1),
    )
    assert test_system_a_prime == test_system_a_secunde
