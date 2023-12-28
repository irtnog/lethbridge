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

import importlib
import logging
import pkgutil
from configparser import ConfigParser
from io import StringIO
from logging.config import dictConfig
from pathlib import Path
from typing import Annotated, Optional

import typer
import typer.core

from .. import ERRORS, __app_name__, __version__
from ..config import CONFIG_FILE_PATH, DEFAULT_CONFIG, load_config

# configure module-level logging
logger = logging.getLogger(__name__)

# disable Rich; cf.
# https://github.com/tiangolo/typer/pull/647#issuecomment-1868190451
typer.core.rich = None

# create the CLI
app = typer.Typer(pretty_exceptions_enable=False)

# load CLI commands from submodules
__path__ = pkgutil.extend_path(__path__, __name__)  # noqa: F821
[
    (
        lambda _cmd, _name, _help: app.add_typer(_cmd, name=_name, help=_help)
        if isinstance(_cmd, typer.Typer)
        else None
    )(
        getattr(_module, "app", None),
        _module.__name__.split(".")[-1],
        getattr(_module, "help", None),
    )
    for _module in [
        importlib.import_module(_modname)
        for _importer, _modname, _ispkg in pkgutil.walk_packages(
            path=__path__, prefix=__name__ + "."
        )
    ]
]


@app.command()
def listen() -> None:
    """Connect to the Elite Dangerous Data Network (EDDN)."""
    pass


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(
            f"{__app_name__} {__version__}, "
            + "a free/libre/open source client for EDDN (and more)"
        )
        typer.echo("Copyright (C) 2023  Matthew X. Economou")
        typer.echo(
            "License AGPLv3+: GNU AGPL version 3 or later "
            + "<https://www.gnu.org/licenses/agpl.html>."
        )
        typer.echo(
            "Source code for this version can be found at "
            + "<https://github.com/irtnog/lethbridge>."
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
    init_file: Annotated[
        Optional[Path],
        typer.Option(
            "--init",
            "-i",
            help="Override the default initialization file.",
        ),
    ] = None,
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
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "loggers": {
                "alembic": {
                    "level": "DEBUG" if debug else "INFO" if verbose else "WARNING",
                    "propagate": 1,
                },
                "lethbridge": {
                    "level": "DEBUG" if debug else "INFO" if verbose else "WARNING",
                    "propagate": 1,
                },
                "sqlalchemy.engine": {
                    "level": "DEBUG" if debug else "INFO" if verbose else "WARNING",
                    "propagate": 1,
                },
            },
            "root": {
                "level": "DEBUG" if debug else "INFO" if verbose else "WARNING",
                "handlers": ["console"] if not quiet else [],
            },
        }
    )

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

    # run the initialization file
    if not init_file:
        init_file = app_cfg["cli"]["init_file"]
    try:
        exec(compile(open(init_file, "rb").read(), init_file, "exec"))
    except FileNotFoundError as e:
        logger.debug(e)
    except Exception as e:
        logger.warning(e)
    return
