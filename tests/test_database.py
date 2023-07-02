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
from lethbridge import SUCCESS
from lethbridge.database import System
from lethbridge.database import init_database
from psycopg2cffi import compat
from pytest import fixture
from pytest import mark
from pytest import param
from pytest import raises
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

# invoke psycopg2cffi compatibility hook
compat.register()


@fixture
def mock_postgresql(postgresql):
    return f'postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}'


@fixture(scope='session')
def mock_sqlite(tmp_path_factory):
    sqlite_path = tmp_path_factory.mktemp('db') / 'galaxy.sqlite'
    return ('sqlite:///' + str(sqlite_path))


@mark.parametrize(
    'db_uri_fixture',
    [
        param('mock_sqlite'),
        param('mock_postgresql'),
    ],
)
def test_orm_basic(db_uri_fixture, request):
    db_uri = request.getfixturevalue(db_uri_fixture)
    init_database_error = init_database(db_uri)
    assert init_database_error == SUCCESS

    engine = create_engine(db_uri)
    Session = sessionmaker(engine)
    with Session.begin() as session:
        new_system = System(
            id64=0,
            name='Test System',
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
                name='Bad System',
                x=1.0,
                y=2.0,
                z=3.0,
                date=datetime(1970, 1, 1, 0, 0),
            )
            session.add(bad_system)

    with Session.begin() as session:
        stmt = select(System).where(System.name.ilike('%test%'))
        existing_system = session.scalars(stmt).one()
        assert existing_system.name == 'Test System'
