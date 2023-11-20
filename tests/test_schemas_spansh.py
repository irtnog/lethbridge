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

from collections import deque
from dateutil.parser import parse
from itertools import zip_longest
from lethbridge.database import System
from lethbridge.schemas.spansh import SystemSchema
from operator import itemgetter
from operator import methodcaller
from pytest import mark
import warnings


@mark.slow
def test_spansh_systemschema(mock_session, mock_galaxy_data, utilities):
    for load_data in mock_galaxy_data:
        with mock_session.begin() as session:
            new_system = SystemSchema().load(load_data, session=session)
            session.add(new_system)

        with mock_session.begin() as session:
            new_system = session.get(System, load_data["id64"])
            dump_data = SystemSchema().dump(new_system)

        # walk source and output data in parallel, depth first,
        # comparing each pair of source/output nodes along the way
        stack = deque()
        stack.append((dump_data, load_data, "top level"))
        while stack:
            (to, fro, ctx) = stack.pop()
            if isinstance(to, list):
                assert isinstance(fro, list)
                assert len(to) == len(fro), ctx
                if len(to):
                    # peek at first element to figure out sorting
                    start = next(iter(to))
                    # default to list of strings
                    sorter = None
                    if isinstance(start, dict):
                        if "symbol" in start:
                            # list of commodities
                            sorter = itemgetter("symbol")
                        elif "name" in start:
                            # list of objects
                            sorter = itemgetter("name")
                        else:
                            # list of key/value pairs
                            sorter = methodcaller("__str__")
                    # sort to/fro and pair corresponding elements of each
                    stack.extend(
                        zip_longest(
                            sorted(to, key=sorter),
                            sorted(fro, key=sorter),
                            [],
                            fillvalue=ctx,
                        )
                    )
            elif isinstance(to, dict):
                assert isinstance(fro, dict)
                assert set(to) <= set(fro), ctx
                if "name" in to and "symbol" not in to:
                    ctx = to["name"]
                for k in to:
                    stack.append((to[k], fro[k], ctx))
            else:
                try:
                    # try parsing to/fro as date/time values
                    new_to = parse(to)
                    # try detecting which date/time format Spansh used
                    if "T" in fro:
                        # e.g., "2023-06-12T05:05:24"
                        new_fro = parse(fro)
                    else:
                        # e.g., "2023-06-12 05:05:24+00"
                        new_fro = parse(fro[:-3])
                    # if we got this far, it worked
                    to = new_to
                    fro = new_fro
                except:  # noqa: E722
                    pass
                with warnings.catch_warnings():
                    # suppress the warning about an approximate match
                    warnings.simplefilter("ignore")
                    assert utilities.approximately(to, fro), ctx
