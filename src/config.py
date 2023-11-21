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
from configparser import ConfigParser
from pathlib import Path

import typer

from . import CONFIG_ERROR, SUCCESS, __app_name__

# configure module-level logging
logger = logging.getLogger(__name__)

# defaults
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"
INIT_FILE_PATH = CONFIG_DIR_PATH / "init.py"
DEFAULT_CONFIG = ConfigParser()
DEFAULT_CONFIG["cli"] = {
    "init_file": INIT_FILE_PATH,
}
DEFAULT_CONFIG["database"] = {
    "uri": "sqlite:///galaxy.sqlite",
}


def load_config(config_file: Path, existing_cfg: ConfigParser) -> int:
    """Merge the configuration file with an existing configuration."""
    try:
        if config_file.exists():
            logger.debug(f"Configuration file {config_file} exists; loading.")
            existing_cfg.read(config_file)
        else:
            logger.debug(f"Configuration file {config_file} does not exist; skipping.")
    except Exception as e:
        logger.error(f"Could not read or parse {config_file}.")
        logger.info(e)
        return CONFIG_ERROR
    return SUCCESS


def save_config(config_file: Path, new_cfg: ConfigParser) -> int:
    """Save the new configuration to a file."""
    try:
        logger.debug(
            f"Making the directory {config_file.parent} (if it does not exist)."
        )
        config_file.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Touching the configuration file {config_file}.")
        config_file.touch(exist_ok=True)
        logger.debug("Writing the configuration.")
        with config_file.open("w") as file:
            new_cfg.write(file)
    except Exception as e:
        logger.info(e)
        return CONFIG_ERROR
    return SUCCESS
