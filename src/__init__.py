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
from importlib.metadata import version

__app_name__ = __name__
__version__ = version(__app_name__)

# configure module-level logging
logger = logging.getLogger(__name__)

# exit codes
(  # TODO: better exit codes
    SUCCESS,
    CONFIG_ERROR,
    DATABASE_ERROR,
) = range(3)

ERRORS = {  # TODO: better error messages
    CONFIG_ERROR: "Configuration error",
    DATABASE_ERROR: "Database error",
}
