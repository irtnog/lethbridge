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

from configparser import ConfigParser
from typing import Annotated, Optional

import typer
from click.exceptions import MissingParameter

from .. import CONFIG_ERROR, ERRORS
from ..config import load_config, save_config

# create the CLI
app = typer.Typer()
help = "Inspect or modify Lethbridge CLI options."


@app.command()
def get(
    ctx: typer.Context,
    section: Annotated[
        str,
        typer.Argument(
            help="Find the setting in this part of the configuration.",
        ),
    ],
    option: Annotated[
        str,
        typer.Argument(
            help="The name of the setting.",
        ),
    ],
) -> None:
    """Print the current configuration."""
    app_cfg = ctx.obj["app_cfg"]
    if not app_cfg.has_option(section, option):
        typer.secho("Invalid section or option.", fg=typer.colors.RED)
        raise typer.Exit(CONFIG_ERROR)
    typer.secho(app_cfg.get(section, option, raw=True))


@app.command()
def set(
    ctx: typer.Context,
    section: Annotated[
        str,
        typer.Argument(
            help="Find the setting in this part of the configuration.",
        ),
    ],
    option: Annotated[
        str,
        typer.Argument(
            help="The name of the setting.",
        ),
    ],
    value: Annotated[
        Optional[str],
        typer.Argument(
            help="The setting's new value.",
        ),
    ] = None,
    reset: Annotated[
        bool,
        typer.Option(
            "--reset",
            help="Reset this setting to its default value.  Any new value is ignored.",
        ),
    ] = False,
) -> None:
    """Change the value of a setting."""
    app_cfg = ctx.obj["app_cfg"]
    if not app_cfg.has_option(section, option):
        typer.secho("Invalid section or option.", fg=typer.colors.RED)
        raise typer.Exit(CONFIG_ERROR)

    # don't persist the defaults because what if they change? so load
    # just the previously changed settings
    new_cfg = ConfigParser()
    config_file = ctx.obj["config_file"]
    load_config_error = load_config(config_file, new_cfg)
    if load_config_error:
        typer.secho(ERRORS[load_config_error], fg=typer.colors.RED)
        raise typer.Exit(load_config_error)

    # get the section into a known state
    if section not in new_cfg.sections():
        new_cfg[section] = {}

    # add/remove the setting
    if value is None and not reset:
        raise MissingParameter(param_type="argument", param_hint="'VALUE'")
    elif reset:
        try:
            new_cfg[section].pop(option)
        except KeyError:
            pass
    else:
        # only save settings that changed
        if app_cfg.get(section, option, raw=True) == value:
            return
        new_cfg[section][option] = value

    # remove the section if it's empty
    if len(new_cfg[section]) == 0:
        new_cfg.remove_section(section)

    # write the new config to disk (it's ok to be empty)
    save_config_error = save_config(config_file, new_cfg)
    if save_config_error:
        typer.secho(ERRORS[save_config_error], fg=typer.colors.RED)
        raise typer.Exit(save_config_error)
