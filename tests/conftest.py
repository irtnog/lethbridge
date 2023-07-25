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

from pathlib import Path
from pytest import fixture
from pytest import mark
from pytest import param
import simplejson as json


# Invoke smoke tests with `pytest -k smoke -x`.  See also
# https://docs.pytest.org/en/stable/mark.html,
# https://stackoverflow.com/a/52369721,
# https://docs.pytest.org/en/stable/how-to/fixtures.html#parametrizing-fixtures,
# https://docs.pytest.org/en/stable/how-to/fixtures.html#using-marks-with-parametrized-fixtures
@fixture(
    params=[
        "postgresql",
        param("sqlite", marks=mark.smoke),
    ],
)
def mock_db_uri(postgresql, tmp_path_factory, request):
    if request.param == "postgresql":
        yield (
            f"postgresql+psycopg2://{postgresql.info.user}"
            + f":@{postgresql.info.host}"
            + f":{postgresql.info.port}"
            + f"/{postgresql.info.dbname}"
            + "?options=-c timezone=utc"
        )
    elif request.param == "sqlite":
        db_path = tmp_path_factory.mktemp("db") / "galaxy.sqlite"
        yield f"sqlite:///{db_path}"


@fixture(scope="module")
def mock_galaxy_data():
    data_file = Path(__file__).parent / "galaxy.json"
    yield json.loads(data_file.read_text(), use_decimal=True)
