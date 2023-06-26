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

from . import __app_name__
from . import CONFIG_ERROR
from . import SUCCESS
from pathlib import Path
import configparser
import logging
import typer

# configure module-level logging
logger = logging.getLogger(__name__)

# defaults
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / 'config.ini'
configuration = configparser.ConfigParser()
configuration['database'] = {
    'uri': 'sqlite:///' + str(CONFIG_DIR_PATH / 'galaxy.sqlite')
}


def init_config(config_file: Path) -> int:
    # create the configuration file if it doesn't already exist
    try:
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.touch(exist_ok=True)
    except Exception as e:
        logger.info(e)
        return CONFIG_ERROR
    return SUCCESS


def load_config(config_file: Path) -> int:
    # make sure the configuration file exists first
    init_config_error = init_config(config_file)
    if init_config_error:
        return init_config_error

    # merge the configuration file with the defaults
    try:
        configuration.read(config_file)
    except Exception as e:
        logger.warning(f'Could not read configuration file: {config_file}')
        logger.info(e)
        pass
    return SUCCESS


def save_config(config_file: Path) -> int:
    # make sure the configuration file exists first
    init_config_error = init_config(config_file)
    if init_config_error:
        return init_config_error

    # save the current configuration
    try:
        with config_file.open('w') as file:
            configuration.write(file)
    except Exception as e:
        logger.info(e)
        return CONFIG_ERROR
    return SUCCESS
