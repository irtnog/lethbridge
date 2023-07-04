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
from ..database import init_database
from typing import Annotated
from typing import Optional
import typer

# create the CLI
app = typer.Typer()
help = "Manage the database back end."


@app.command()
def init(
    ctx: typer.Context,
    uri: Annotated[
        Optional[str],
        typer.Argument(
            help="Connect to the specified database instead of the configured default.  Refer to <https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls> for the format.",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            help="Force database re-initialization.",
        ),
    ] = False,
) -> None:
    """Initialze the database, creating tables, views, etc."""
    app_cfg = ctx.obj["app_cfg"]
    if not uri:
        uri = app_cfg["database"]["uri"]
    init_database_error = init_database(uri, force)
    if init_database_error:
        typer.secho(ERRORS[init_database_error], fg=typer.colors.RED)
        raise typer.Exit(init_database_error)
    typer.secho("Initialization succeeded.", fg=typer.colors.GREEN)
