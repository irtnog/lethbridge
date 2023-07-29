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
from lethbridge import __app_name__
from lethbridge import __version__
from lethbridge import cli
from lethbridge.config import DEFAULT_CONFIG
from pytest import fixture
from pytest import mark
from pytest import param
from typer import Typer
from typer.testing import CliRunner

runner = CliRunner()

INITIAL_CONFIG = "[database]\nuri = some+test://database\n\n"
MODIFIED_CONFIG = "[database]\nuri = another://uri\n\n"
INIT_CODE = 'print("Initialization worked.")\n'
BAD_CODE = "foobar()\n"


@fixture(scope="session")
def mock_config_file(tmp_path_factory):
    cfg_file_path = tmp_path_factory.mktemp("etc") / "config.ini"
    cfg_file_path.write_text(INITIAL_CONFIG)
    return cfg_file_path


@fixture(scope="session")
def mock_empty_config(tmp_path_factory):
    cfg_file_path = tmp_path_factory.mktemp("etc") / "empty.ini"
    cfg_file_path.touch()
    return cfg_file_path


@fixture(scope="session")
def mock_empty_init(tmp_path_factory):
    init_file_path = tmp_path_factory.mktemp("etc") / "empty-init.py"
    init_file_path.touch()
    return init_file_path


@fixture(scope="session")
def mock_init_file(tmp_path_factory):
    init_file_path = tmp_path_factory.mktemp("etc") / "init.py"
    init_file_path.write_text(INIT_CODE)
    return init_file_path


@fixture(scope="session")
def mock_bad_init(tmp_path_factory):
    init_file_path = tmp_path_factory.mktemp("etc") / "bad-init.py"
    init_file_path.write_text(BAD_CODE)
    return init_file_path


@fixture(scope="session")
def mock_missing_init(tmp_path_factory):
    init_file_path = tmp_path_factory.mktemp("etc") / "missing-init.py"
    return init_file_path


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} {__version__}" in result.stdout


def test_cli_autoloader():
    assert "configure" in cli.__dict__
    assert isinstance(cli.configure.app, Typer)


@mark.parametrize(
    "section, option, expected_error, expected_output",
    [
        param("database", "uri", SUCCESS, "some+test://database"),
        param("database", "url", CONFIG_ERROR, "Invalid section or option."),
        param("dalebase", "uri", CONFIG_ERROR, "Invalid section or option."),
        param("dalebase", None, 2, "Error: Missing argument"),
        param(None, None, 2, "Error: Missing argument"),
    ],
)
def test_cli_configure_get(
    mock_config_file, mock_empty_init, section, option, expected_error, expected_output
):
    get_cmd = ["-f", mock_config_file, "-i", mock_empty_init, "configure", "get"]
    if section is not None:
        get_cmd += [section]
        if option is not None:
            get_cmd += [option]
    result = runner.invoke(cli.app, get_cmd)
    assert result.exit_code == expected_error
    assert expected_output in result.stdout


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
    mock_config_file,
    mock_empty_init,
    section,
    option,
    value,
    reset,
    expected_error,
    expected_config,
):
    set_cmd = ["-f", mock_config_file, "-i", mock_empty_init, "configure", "set"]
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


def test_cli_configure_set_noop(mock_empty_config, mock_empty_init):
    set_cmd = [
        "-f",
        mock_empty_config,
        "-i",
        mock_empty_init,
        "configure",
        "set",
        "database",
        "uri",
        DEFAULT_CONFIG["database"]["uri"],
    ]
    result = runner.invoke(cli.app, set_cmd)
    assert result.exit_code == SUCCESS
    assert "" == mock_empty_config.read_text()


@mark.parametrize(
    "init_file_fixture, expected_error, expected_output",
    [
        param("mock_init_file", SUCCESS, "Initialization worked."),
        param("mock_bad_init", SUCCESS, ""),
        param("mock_missing_init", SUCCESS, ""),
    ],
)
def test_cli_init_file(
    mock_empty_config, init_file_fixture, expected_error, expected_output, request
):
    init_file = request.getfixturevalue(init_file_fixture)
    cmd = [
        "-f",
        mock_empty_config,
        "-i",
        init_file,
        "configure",
        "--help",
    ]
    result = runner.invoke(cli.app, cmd)
    assert result.exit_code == expected_error
    assert expected_output in result.stdout
