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

from typing import Annotated, Optional

import alembic.command
import alembic.config
import typer

# create the CLI
app = typer.Typer()
help = "Manage the database back end."


@app.command()
def current(ctx: typer.Context) -> None:
    """Display the current database revision."""
    alembic_cfg = ctx.obj["alembic_cfg"]
    alembic.command.current(alembic_cfg, True)


@app.command()
def downgrade(
    ctx: typer.Context,
    revision: Annotated[
        str,
        typer.Argument(
            help="The database schema revision identifier.  For more information, "
            + "refer to <https://alembic.sqlalchemy.org/en/latest/tutorial.html>.",
        ),
    ],
    sql: Annotated[
        Optional[bool],
        typer.Option(
            "--sql",
            help="Do not modify the database.  Instead, output the SQL statements "
            + "that would have been executed.  For more information, refer to "
            + "<https://alembic.sqlalchemy.org/en/latest/offline.html>.",
        ),
    ] = None,
) -> None:
    """Revert to a previous version of the database schema."""
    alembic_cfg = ctx.obj["alembic_cfg"]
    alembic.command.downgrade(alembic_cfg, revision, sql=sql)


@app.command()
def history(
    ctx: typer.Context,
    rev_range: Annotated[
        Optional[str],
        typer.Argument(
            help="Starting and ending database schema revisions, separated by a colon, "
            + "e.g., `1975ea:ae1027`.  Symbols like `head`, `heads`, `base`, or "
            + "`current` may be used, as can negative relative ranges for the starting "
            + "revision and positive relative ranges for the ending revision.  For "
            + "more information, refer to "
            + "<https://alembic.sqlalchemy.org/en/latest/tutorial.html#viewing-history-ranges>.",  # noqa: E501
        ),
    ] = None,
    indicate_current: Annotated[
        Optional[bool],
        typer.Option(
            "--show-current",
            help="Indicate the database's current schema revision.",
        ),
    ] = None,
) -> None:
    """List database schema revisions (changeset scripts) in
    chronological order."""
    alembic_cfg = ctx.obj["alembic_cfg"]
    alembic.command.history(alembic_cfg, rev_range, True, indicate_current)


@app.command()
def show(
    ctx: typer.Context,
    revision: Annotated[
        str,
        typer.Argument(
            help="The database schema revision identifier.  For more information, "
            + "refer to <https://alembic.sqlalchemy.org/en/latest/tutorial.html>.",
        ),
    ],
) -> None:
    """Show the indicated version of the database schema."""
    alembic_cfg = ctx.obj["alembic_cfg"]
    alembic.command.show(alembic_cfg, revision)


@app.command()
def stamp(
    ctx: typer.Context,
    revision: Annotated[
        str,
        typer.Argument(
            help="The database schema revision identifier.  For more information, "
            + "refer to <https://alembic.sqlalchemy.org/en/latest/tutorial.html>.",
        ),
    ],
    sql: Annotated[
        Optional[bool],
        typer.Option(
            "--sql",
            help="Do not modify the database.  Instead, output the SQL statements that "
            + "would have been executed.  For more information, refer to "
            + "<https://alembic.sqlalchemy.org/en/latest/offline.html>.",
        ),
    ] = None,
    purge: Annotated[
        Optional[bool],
        typer.Option(
            "--purge",
            help="Delete all entries in the version table before stamping.",
        ),
    ] = None,
) -> None:
    """Mark the database as being at the given schema version, but do
    not run any migrations."""
    alembic_cfg = ctx.obj["alembic_cfg"]
    alembic.command.stamp(alembic_cfg, revision, sql=sql, purge=purge)


@app.command()
def upgrade(
    ctx: typer.Context,
    revision: Annotated[
        str,
        typer.Argument(
            help="The database schema revision identifier.  For more information, "
            + "refer to <https://alembic.sqlalchemy.org/en/latest/tutorial.html>.",
        ),
    ],
    sql: Annotated[
        Optional[bool],
        typer.Option(
            "--sql",
            help="Do not modify the database.  Instead, output the SQL statements that "
            + "would have been executed.  For more information, refer to "
            + "<https://alembic.sqlalchemy.org/en/latest/offline.html>.",
        ),
    ] = None,
) -> None:
    """Upgrade to the specified version of the database schema."""
    alembic_cfg = ctx.obj["alembic_cfg"]
    alembic.command.upgrade(alembic_cfg, revision, sql=sql)


@app.callback()
def main(ctx: typer.Context) -> None:
    app_cfg = ctx.obj["app_cfg"]
    db_uri = app_cfg["database"]["uri"]

    # must match alembic.ini's database list, otherwise Alembic won't
    # find the migrations for this database
    db_type = "postgresql" if db_uri.startswith("postgres") else "sqlite"

    # create the run-time Alembic configuration
    alembic_cfg = alembic.config.Config()
    alembic_cfg.set_main_option("script_location", "lethbridge:migrations")
    alembic_cfg.set_main_option("databases", db_type)
    alembic_cfg.set_section_option(db_type, "sqlalchemy.url", db_uri)
    ctx.obj["alembic_cfg"] = alembic_cfg
