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
DEFAULT_DATABASE_URI = 'sqlite:///' + str(CONFIG_DIR_PATH / 'galaxy.sqlite')


def _init_config(config_file: Path) -> int:
    try:
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.touch(exist_ok=True)
    except Exception as e:
        logger.debug(e)
        return CONFIG_ERROR
    return SUCCESS


def get_database_uri(config_file: Path) -> str:
    '''Return the current database connection information.'''
    cfg = configparser.ConfigParser()
    try:
        cfg.read(config_file)
    except Exception as e:
        logger.warning(e)
        pass
    return cfg.get('database', 'uri', fallback=DEFAULT_DATABASE_URI)


def set_database_uri(config_file: Path, database_uri: str) -> int:
    # TODO: validate database_uri
    init_config_error = _init_config(config_file)
    if init_config_error:
        return init_config_error

    cfg = configparser.ConfigParser()
    try:
        cfg.read(config_file)
    except Exception as e:
        logger.debug(e)
        return CONFIG_ERROR

    if 'database' not in cfg:
        cfg['database'] = {}
    if database_uri:
        cfg['database']['uri'] = database_uri
    else:
        # remove from config if false-ish
        cfg['database'].pop('uri', None)

    try:
        with config_file.open('w') as file:
            cfg.write(file)
    except Exception as e:
        logger.debug(e)
        return CONFIG_ERROR
    return SUCCESS
