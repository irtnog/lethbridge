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

from ..config import CONFIG_FILE_PATH
from .. import __app_name__
from .. import __version__
from pathlib import Path
from typing import Optional
import logging
import typer

# configure module-level logging
logger = logging.getLogger(__name__)

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} {__version__}, a free/libre/open source client for EDDN (and more)')
        typer.echo('Copyright (C) 2023  Matthew X. Economou')
        typer.echo('License AGPLv3+: GNU AGPL version 3 or later <https://www.gnu.org/licenses/agpl.html>.')
        typer.echo('Source code for this version can be found at <https://github.com/irtnog/lethbridge>.')
        raise typer.Exit()


@app.callback()
def main(
        config: Optional[Path] = typer.Option(
            CONFIG_FILE_PATH,
            '--config',
            '-f',
            help='Override the default configuration file.',
        ),
        version: Optional[bool] = typer.Option(
            None,
            '--version',
            '-v',
            help='Show the application\'s version and exit.',
            callback=_version_callback,
            is_eager=True
        ),
) -> None:
    if config:
        CONFIG_FILE_PATH = config  # noqa: F841
    return
