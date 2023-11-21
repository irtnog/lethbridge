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

from configparser import ConfigParser

from pytest import fixture, mark, param

from lethbridge import CONFIG_ERROR, SUCCESS
from lethbridge.config import load_config, save_config


# FIXME: find a more reliable way to mock this
@fixture
def mock_inaccessible_file(tmp_path):
    return "/inaccessible/config.ini"


@mark.parametrize(
    "config_file_fixture, expected_error",
    [
        param("mock_inaccessible_file", CONFIG_ERROR),
        param("mock_config_file", SUCCESS),
    ],
)
def test_load_config(config_file_fixture, expected_error, request):
    config_file = request.getfixturevalue(config_file_fixture)
    new_cfg = ConfigParser()
    load_config_error = load_config(config_file, new_cfg)
    assert load_config_error == expected_error


@mark.parametrize(
    "config_file_fixture, expected_error",
    [
        param("mock_inaccessible_file", CONFIG_ERROR),
        param("mock_config_file", SUCCESS),
    ],
)
def test_save_config(config_file_fixture, expected_error, request):
    config_file = request.getfixturevalue(config_file_fixture)
    new_cfg = ConfigParser()
    new_cfg["database"] = {"uri": "sqlite://"}
    save_config_error = save_config(config_file, new_cfg)
    assert save_config_error == expected_error
