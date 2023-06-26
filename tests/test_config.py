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
from lethbridge.config import init_config
from lethbridge.config import load_config
from lethbridge.config import save_config
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
    'config_file_fixture, expected_error',
    [
        param('mock_inaccessible_file', CONFIG_ERROR),
        param('mock_config_file', SUCCESS),
    ],
)
def test_init_config(config_file_fixture, expected_error, request):
    config_file = request.getfixturevalue(config_file_fixture)
    init_config_error = init_config(config_file)
    assert init_config_error == expected_error


@mark.parametrize(
    'config_file_fixture, expected_error',
    [
        param('mock_inaccessible_file', CONFIG_ERROR),
        param('mock_config_file', SUCCESS),
    ],
)
def test_load_config(config_file_fixture, expected_error, request):
    config_file = request.getfixturevalue(config_file_fixture)
    load_config_error = load_config(config_file)
    assert load_config_error == expected_error


@mark.parametrize(
    'config_file_fixture, expected_error',
    [
        param('mock_inaccessible_file', CONFIG_ERROR),
        param('mock_config_file', SUCCESS),
    ],
)
def test_save_config(config_file_fixture, expected_error, request):
    config_file = request.getfixturevalue(config_file_fixture)
    save_config_error = save_config(config_file)
    assert save_config_error == expected_error
