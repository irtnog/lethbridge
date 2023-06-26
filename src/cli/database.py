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

from .. import ERRORS
from ..config import configuration
from ..database import init_database
import typer

# create the CLI
app = typer.Typer()
help = 'Manage the database back end.'


@app.command()
def init(
        uri: str = typer.Option(
            configuration['database']['uri'],
            '--uri',
            '-u',
            help='Connect to the specified database.  Refer to <https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls> for the format.',
        ),
        force: bool = typer.Option(
            False,
            '--force',
            help='Force database re-initialization.',
        ),
) -> None:
    '''Initialze the database, creating tables, views, etc.'''
    init_database_error = init_database(uri, force)
    if init_database_error:
        typer.secho(ERRORS[init_database_error], fg=typer.colors.RED)
        raise typer.Exit(init_database_error)
    typer.secho('Initialization succeeded.', fg=typer.colors.GREEN)
