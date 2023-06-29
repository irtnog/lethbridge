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

from ..config import configuration
from typing import Annotated
from typing import Optional
import typer

# create the CLI
app = typer.Typer()
help = 'Inspect or modify Lethbridge CLI options.'


@app.command()
def get(
        section: Annotated[str, typer.Argument(
            help='Find the setting in this part of the configuration.',
        )],
        option: Annotated[str, typer.Argument(
            help='The name of the setting.',
        )],
) -> None:
    '''Print the current configuration.'''
    if section and key:
        pass
    elif section:
        pass
    else:
        pass


@app.command()
def set(
        section: Annotated[str, typer.Argument(
            help='Find the setting in this part of the configuration.',
        )],
        option: Annotated[str, typer.Argument(
            help='The name of the setting.',
        )],
        value: Annotated[Optional[str], typer.Argument(
            help='The setting\'s new value.',
        )] = None,
        reset: Annotated[bool, typer.Option(
            '--reset',
            help='Reset this setting to its default value.  Any new value is ignored.'
        )] = False,
) -> None:
    '''Change the value of a setting.'''
    # TODO new_cfg.read_string(f'[{section}]\n{key} = {value}')
    pass
