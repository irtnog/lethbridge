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

from pytest import mark, param
from typer import Typer
from typer.testing import CliRunner

from lethbridge import SUCCESS, __app_name__, __version__, cli

runner = CliRunner()


@mark.order("second_to_last")
def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} {__version__}" in result.stdout


@mark.order("second_to_last")
def test_cli_autoloader():
    assert "configure" in cli.__dict__
    assert isinstance(cli.configure.app, Typer)


INIT_OUTPUT = "The init file sends its regards."


@mark.order("second_to_last")
@mark.parametrize(
    "contents, expected_error, expected_output",
    [
        param("", SUCCESS, ""),
        param(None, SUCCESS, ""),
        param(f"print({INIT_OUTPUT!r})\n", SUCCESS, INIT_OUTPUT),
        param("this_init_file_is_broken()\n", SUCCESS, ""),
    ],
)
def test_cli_init_file(tmp_path, contents, expected_error, expected_output):
    init_file = tmp_path / "init.py"
    assert init_file.exists() is False, "sanity check"
    if contents is not None:
        init_file.write_text(contents)
    cmd = ["-i", init_file, "configure", "--help"]
    result = runner.invoke(cli.app, cmd)
    assert result.exit_code == expected_error
    assert expected_output in result.stdout
