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

import warnings
from collections import deque
from itertools import zip_longest
from operator import itemgetter, methodcaller

from dateutil.parser import parse
from pytest import mark, param

from lethbridge.database import System
from lethbridge.schemas.spansh import SystemSchema


@mark.parametrize(
    "galaxy_data_fixture",
    [
        param("mock_galaxy_data_small"),
        param("mock_galaxy_data", marks=mark.slow),
    ],
)
def test_systemschema_load_and_dump(
    mock_session, utilities, galaxy_data_fixture, request
):
    for load_data in request.getfixturevalue(galaxy_data_fixture):
        try:
            with mock_session.begin() as session:
                new_system = SystemSchema().load(load_data, session=session)
                session.add(new_system)
        except Exception as e:
            # add system name/id64 to error message for diagnostics
            raise (type(e))(f"Loading {load_data['name']} ({load_data['id64']}): {e}")

        # Note that the sqlalchemy.exc.SAWarning "Object of
        # type... not in session, add operation along... will not
        # proceed" is expected behavior during a relationship cascade
        # per the following, but I can't figure out how to suppress
        # just that warning without breaking other things.
        #
        # https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-save-update,
        # https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-merge,
        # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge,
        # https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#unitofwork-merging,
        # https://github.com/sqlalchemy/sqlalchemy/discussions/8172,
        # https://github.com/sqlalchemy/sqlalchemy/blob/2458ceee94e7bd6e5bf8d9d7270be8819bbe772c/lib/sqlalchemy/orm/unitofwork.py#L321

        with mock_session.begin() as session:
            new_system = session.get(System, load_data["id64"])
            assert isinstance(new_system, System)
            dump_data = SystemSchema().dump(new_system)
            assert isinstance(dump_data, dict)

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
