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

import logging
from pathlib import Path
from typing import Annotated, Optional

import simplejson as json
import typer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..schemas.spansh import SystemSchema

# configure module-level logging
logger = logging.getLogger(__name__)

# create the CLI
app = typer.Typer()
help = "Import data from non-EDDN sources."


@app.command()
def status() -> None:
    pass


@app.command()
def spansh(
    ctx: typer.Context,
    dataset: Annotated[
        str,
        typer.Argument(
            help="Which dataset to import, e.g., galaxy_7days.  For the list of "
            + "available datasets, refer to <https://www.spansh.co.uk/dumps>.  If this "
            + "is a valid filename or URL, the dataset will be loaded from that "
            + "location, instead."
        ),
    ],
    foreground: Annotated[
        Optional[bool],
        typer.Option(
            "--foreground",
            "--fg",
            help="Perform the import now, interactively, instead of queuing to run in "
            + "the background.",
        ),
    ] = None,
) -> None:
    """Import galaxy or system data from a Spansh data dump."""
    if not foreground:
        typer.secho("FIXME: Background import not implemented", fg=typer.colors.RED)
        raise typer.Exit(-1)
    app_cfg = ctx.obj["app_cfg"]

    # get a handle on the dataset
    datafile = None
    try:
        # can we parse this as a filename?
        datafile = Path(dataset)
    except:  # noqa: E722
        # it's ok if we can't
        pass
    if datafile and datafile.exists():
        ds = datafile.open()
    elif dataset.startswith(("file:", "http:", "https:")):
        typer.secho("FIXME: Import from URLs not implemented", fg=typer.colors.RED)
        raise typer.Exit(-1)
    else:
        typer.secho("FIXME: Import from Spansh not implemented", fg=typer.colors.RED)
        raise typer.Exit(-1)

    engine = create_engine(app_cfg["database"]["uri"])
    Session = sessionmaker(engine)
    next(ds)  # first line is an opening bracket
    for load_data in ds:
        if load_data[0] == "]":
            break
        if load_data.endswith("\n"):
            load_data = load_data[:-1]
        if load_data.endswith(","):
            load_data = load_data[:-1]
        logger.debug(load_data[:50] + "..." if len(load_data) > 50 else load_data)
        try:
            with Session.begin() as session:
                # FIXME: add session support to Schema.loads() in
                # marshmallow-sqlalchemy
                new_system = SystemSchema().load(
                    json.loads(load_data, use_decimal=True), session=session
                )
                typer.secho(f"Importing {new_system!r}")
                session.add(new_system)
        except Exception as e:
            logger.error(e)
    typer.secho("Import complete.", fg=typer.colors.GREEN)


@app.command()
def canonn(
    dataset: Annotated[str, typer.Argument(help="Which dataset to import.")],
    foreground: Annotated[
        Optional[bool],
        typer.Option(
            "--foreground",
            "--fg",
            help="Perform the import now, interactively, instead of queuing to run in "
            + "the background.",
        ),
    ] = None,
) -> None:
    """Import the specified points of interest from a Canonn database."""
    pass


@app.command()
def edtools(
    dataset: Annotated[str, typer.Argument(help="Which dataset to import.")],
    foreground: Annotated[
        Optional[bool],
        typer.Option(
            "--foreground",
            "--fg",
            help="Perform the import now, interactively, instead of queuing to run in "
            + "the background.",
        ),
    ] = None,
) -> None:
    """Import the specified dataset from the Elite:Dangerous tools
    collection.  For the list of available datasets, refer to
    <https://edtools.cc/list.php>."""
    pass
