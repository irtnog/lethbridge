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

from lethbridge import CONFIG_ERROR
from lethbridge import SUCCESS
from lethbridge.config import DEFAULT_DATABASE_URI
from lethbridge.config import get_database_uri
from lethbridge.config import set_database_uri
from pytest import fixture
from pytest import param
from pytest import mark


# FIXME: find a more reliable way to mock this
@fixture
def mock_inaccessible_file(tmp_path):
    return '/inaccessible/config.ini'


@fixture
def mock_config_file(tmp_path):
    config_file = tmp_path / 'config.ini'
    config_file.touch()
    return config_file


@mark.parametrize(
    'config_file, database_uri, expected_error, expected_uri',
    [
        param('mock_inaccessible_file', '', CONFIG_ERROR, DEFAULT_DATABASE_URI),
        param('mock_config_file', False, SUCCESS, DEFAULT_DATABASE_URI),
        param('mock_config_file', None, SUCCESS, DEFAULT_DATABASE_URI),
        param('mock_config_file', '', SUCCESS, DEFAULT_DATABASE_URI),
        param('mock_config_file', 'sqlite://', SUCCESS, 'sqlite://'),
        # TODO: validate database_uri
        # param('mock_config_file', 'bad', CONFIG_ERROR, DEFAULT_DATABASE_URI),
    ]
)
def test_database_uri(config_file, database_uri, expected_error, expected_uri, request):
    config_file_fixture = request.getfixturevalue(config_file)
    setter_error = set_database_uri(config_file_fixture, database_uri)
    assert setter_error == expected_error
    db_uri = get_database_uri(config_file_fixture)
    assert db_uri == expected_uri
