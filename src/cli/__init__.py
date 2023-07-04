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
from .. import __app_name__
from .. import __version__
from ..config import CONFIG_FILE_PATH
from ..config import DEFAULT_CONFIG
from ..config import load_config
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from typing import Annotated
from typing import Optional
import importlib
import logging
import pkgutil
import typer

# configure module-level logging
logger = logging.getLogger(__name__)

# create the CLI
app = typer.Typer()

# build a list of submodules
__path__ = pkgutil.extend_path(__path__, __name__)  # noqa: F821
_submodules = [
    _modname
    for _importer, _modname, _ispkg in pkgutil.walk_packages(
        path=__path__, prefix=__name__ + "."
    )
]

# load submodules and add them as CLI subcommands
for _submodule in _submodules:
    _mdl = importlib.import_module(_submodule)

    # respect the module's external symbol list if present
    if "__all__" in _mdl.__dict__:
        _mdl_names = _mdl.__dict__["__all__"]
    else:
        _mdl_names = [_sym for _sym in _mdl.__dict__]

    if "app" in _mdl_names:
        _subcommand = getattr(_mdl, "app")
        if "help" in _mdl_names:
            _help = getattr(_mdl, "help")
        else:
            _help = None
        if isinstance(_subcommand, typer.Typer):
            app.add_typer(_subcommand, name=_submodule.split(".")[-1], help=_help)


@app.command()
def listen() -> None:
    """Connect to the Elite Dangerous Data Network (EDDN)."""
    pass


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(
            f"{__app_name__} {__version__}, a free/libre/open source client for EDDN (and more)"
        )
        typer.echo("Copyright (C) 2023  Matthew X. Economou")
        typer.echo(
            "License AGPLv3+: GNU AGPL version 3 or later <https://www.gnu.org/licenses/agpl.html>."
        )
        typer.echo(
            "Source code for this version can be found at <https://github.com/irtnog/lethbridge>."
        )
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    config_file: Annotated[
        Optional[Path],
        typer.Option(
            "--config",
            "-f",
            help="Override the default configuration file.",
        ),
    ] = CONFIG_FILE_PATH,
    debug: Annotated[
        Optional[bool],
        typer.Option(
            "--debug",
            "-d",
            help="Enable detailed activity tracing.",
        ),
    ] = None,
    quiet: Annotated[
        Optional[bool],
        typer.Option(
            "--quiet",
            "-q",
            help="Silence all program output.",
        ),
    ] = None,
    verbose: Annotated[
        Optional[bool],
        typer.Option(
            "--verbose",
            "-v",
            help="Include backtraces in error messages.",
        ),
    ] = None,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    ctx.obj = {}  # user-defined shared state

    # configure logging
    app_logger = logging.getLogger(__app_name__)
    app_logger.setLevel(
        logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING
    )
    if not quiet:
        cerr = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        cerr.setFormatter(formatter)
        app_logger.addHandler(cerr)

    # copy the default configuration
    config_string = StringIO()
    DEFAULT_CONFIG.write(config_string)
    config_string.seek(0)
    app_cfg = ConfigParser()
    app_cfg.read_file(config_string)

    # load the configuration file (overwrites the defaults)
    load_config_error = load_config(config_file, app_cfg)
    if load_config_error:
        typer.secho(ERRORS[load_config_error], fg=typer.colors.RED)
        raise typer.Exit(load_config_error)

    # pass global state like application configuration to other parts
    # of the UI via Typer's/Click's context object
    ctx.obj["config_file"] = config_file
    ctx.obj["app_cfg"] = app_cfg
    return
