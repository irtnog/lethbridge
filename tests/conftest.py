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

from decimal import Decimal
from lethbridge.database import Base
from math import isclose
from pathlib import Path
from pytest import fixture
from pytest import mark
from pytest import param
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from warnings import warn
import simplejson as json


class Utilities:
    """Helper functions for tests.  Access via the `utilities`
    fixture.  Cf. https://stackoverflow.com/a/42156088."""

    @staticmethod
    def approximately(x, y):
        str_x = str(x)
        str_y = str(y)
        if str_x == str_y:
            return True
        elif (
            str_x in str_y
            or str_y in str_x
            or (
                (isinstance(x, float) or isinstance(x, Decimal))
                and (isinstance(y, float) or isinstance(y, Decimal))
                and isclose(x, y, rel_tol=0.05)
            )
        ):
            warn(f"{str_x!r} only approximately equal to {str_y!r}")
            return True
        else:
            return False


@fixture
def utilities():
    return Utilities


@fixture
def mock_config_file(tmp_path):
    config_file = tmp_path / "config.ini"
    config_file.touch()
    return config_file


@fixture
def mock_init_file(tmp_path):
    init_file = tmp_path / "init.py"
    init_file.touch()
    return init_file


# Invoke smoke tests with `pytest -k smoke -x`.  See also
# https://docs.pytest.org/en/stable/mark.html,
# https://stackoverflow.com/a/52369721,
# https://docs.pytest.org/en/stable/how-to/fixtures.html#parametrizing-fixtures,
# https://docs.pytest.org/en/stable/how-to/fixtures.html#using-marks-with-parametrized-fixtures
@fixture(
    params=[
        param("postgresql", marks=mark.smoke),
        "sqlite",
    ],
)
def mock_db_uri(postgresql, tmp_path, request):
    match request.param:
        case "postgresql":
            yield (
                f"postgresql+psycopg2://{postgresql.info.user}"
                + f":@{postgresql.info.host}"
                + f":{postgresql.info.port}"
                + f"/{postgresql.info.dbname}"
                + "?options=-c timezone=utc"
            )
        case "sqlite":
            yield f"sqlite:///{tmp_path / 'db.sqlite3'}"


@fixture
def mock_cmd_prefix(mock_config_file, mock_init_file, mock_db_uri):
    mock_config_file.write_text(
        f"""[cli]
init_file = {mock_init_file}

[database]
uri = {mock_db_uri}
"""
    )
    return ["-f", mock_config_file]


@fixture
def mock_session(mock_db_uri):
    engine = create_engine(mock_db_uri, poolclass=NullPool)
    Base.metadata.create_all(engine)
    yield sessionmaker(engine)


@fixture(scope="session")
def mock_galaxy_data():
    data_file = Path(__file__).parent / "mock-galaxy-data.json"
    yield json.loads(data_file.read_text(), use_decimal=True)


@fixture(scope="session")
def mock_spansh_import():
    yield str(Path(__file__).parent / "mock-spansh-import.json")


@fixture(scope="session")
def mock_spansh_update():
    yield str(Path(__file__).parent / "mock-spansh-update.json")
