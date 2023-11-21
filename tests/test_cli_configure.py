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

from pytest import fixture, mark, param
from typer.testing import CliRunner

from lethbridge import CONFIG_ERROR, SUCCESS, cli
from lethbridge.config import DEFAULT_CONFIG

runner = CliRunner()

INITIAL_CONFIG = "[database]\nuri = some+test://database\n\n"
MODIFIED_CONFIG = "[database]\nuri = another://uri\n\n"


@fixture(scope="session")
def mock_config_file(tmp_path_factory):
    cfg_file_path = tmp_path_factory.mktemp("etc") / "config.ini"
    cfg_file_path.write_text(INITIAL_CONFIG)
    return cfg_file_path


@mark.order("last")
@mark.parametrize(
    "section, option, expected_error, expected_output",
    [
        param("database", "uri", SUCCESS, "some+test://database"),
        param("database", "url", CONFIG_ERROR, "Invalid section or option."),
        param("dalebase", "uri", CONFIG_ERROR, "Invalid section or option."),
        param("dalebase", None, 2, ""),
        param(None, None, 2, ""),
    ],
)
def test_cli_configure_get(
    mock_config_file, section, option, expected_error, expected_output
):
    get_cmd = ["-f", mock_config_file, "configure", "get"]
    if section is not None:
        get_cmd += [section]
        if option is not None:
            get_cmd += [option]
    result = runner.invoke(cli.app, get_cmd)
    assert result.exit_code == expected_error
    assert expected_output in result.stdout


@mark.order("last")
@mark.parametrize(
    "section, option, value, reset, expected_error, expected_config",
    [
        param("database", "url", "another://uri", None, CONFIG_ERROR, INITIAL_CONFIG),
        param("dalebase", "uri", "another://uri", None, CONFIG_ERROR, INITIAL_CONFIG),
        param("database", "uri", None, None, 2, INITIAL_CONFIG),
        param("database", None, None, None, 2, INITIAL_CONFIG),
        param(None, None, None, None, 2, INITIAL_CONFIG),
        param("database", "uri", "another://uri", True, SUCCESS, ""),
        param("database", "uri", "another://uri", None, SUCCESS, MODIFIED_CONFIG),
        param("database", "uri", None, True, SUCCESS, ""),
    ],
)
def test_cli_configure_set(
    mock_config_file, section, option, value, reset, expected_error, expected_config
):
    set_cmd = ["-f", mock_config_file, "configure", "set"]
    if section is not None:
        set_cmd += [section]
        if option is not None:
            set_cmd += [option]
            if value is not None:
                set_cmd += [value]
    if reset:
        set_cmd += ["--reset"]
    result = runner.invoke(cli.app, set_cmd)
    assert result.exit_code == expected_error
    assert expected_config == mock_config_file.read_text()


@mark.order("last")
def test_cli_configure_set_noop(tmp_path):
    empty_config_file = tmp_path / "empty.ini"
    empty_config_file.touch()
    set_cmd = [
        "-f",
        empty_config_file,
        "configure",
        "set",
        "database",
        "uri",
        DEFAULT_CONFIG["database"]["uri"],
    ]
    result = runner.invoke(cli.app, set_cmd)
    assert result.exit_code == SUCCESS
    assert "" == empty_config_file.read_text()
