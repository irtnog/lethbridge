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

from lethbridge import DATABASE_ERROR
from lethbridge import SUCCESS
from lethbridge import cli
from pytest import mark
from pytest import param
from typer.testing import CliRunner

runner = CliRunner()


@mark.parametrize(
    "uri, force, expected_error",
    [
        param("obvious nonsense", False, DATABASE_ERROR),
        param("sqlite://", False, SUCCESS),
        param("sqlite://", True, SUCCESS),
    ],
)
def test_cli_database_init(uri, force, expected_error):
    cmd = ["database", "init", uri]
    if force:
        cmd += ["--force"]
    result = runner.invoke(cli.app, cmd)
    assert result.exit_code == expected_error
