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
from typing import Annotated
from typing import Optional
import typer

# create the CLI
app = typer.Typer()
help = "Import data from non-EDDN sources."


@app.command()
def status() -> None:
    pass


@app.command()
def spansh(
    dataset: Annotated[
        str,
        typer.Argument(
            help="Which dataset to import, e.g., galaxy_7days.  For the list of available datasets, refer to <https://www.spansh.co.uk/dumps>."
        ),
    ],
    foreground: Annotated[
        Optional[bool],
        typer.Option(
            "--foreground",
            "--fg",
            help="Perform the import now, interactively, instead of queuing to run in the background.",
        ),
    ] = None,
) -> None:
    """Import galaxy or system data from a Spansh data dump."""
    pass


@app.command()
def canonn(
    dataset: Annotated[str, typer.Argument(help="Which dataset to import.")],
    foreground: Annotated[
        Optional[bool],
        typer.Option(
            "--foreground",
            "--fg",
            help="Perform the import now, interactively, instead of queuing to run in the background.",
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
            help="Perform the import now, interactively, instead of queuing to run in the background.",
        ),
    ] = None,
) -> None:
    """Import the specified dataset from the Elite:Dangerous tools collection.  For the list of available datasets, refer to <https://edtools.cc/list.php>."""
    pass
