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

# TODO: an integration test that includes
# 1. Initializing the database (`lethbridge database init`)
# 2. Running the import (`lethbridge import spansh <mock_spansh_import> --foreground`)
# 3. Performing some database queries.
# 4. Running another import with new/updated data.
# 5. Performing some more database queries.

import importlib
from configparser import ConfigParser

import alembic.command
import alembic.config
from pytest import fixture, mark, param
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typer import Context
from typer.core import TyperCommand
from typer.testing import CliRunner

from lethbridge import cli
from lethbridge.database import System

runner = CliRunner()


@fixture
def mock_cmd_prefix_initialized(mock_cmd_prefix):
    # note that mock_cmd_prefix is already parameterized via
    # mock_db_uri (cf. conftest.py), so grab the relevant configs and
    # adjust what would be parameters here on the fly
    app_cfg = ConfigParser()
    app_cfg.read_file(open(mock_cmd_prefix[-1]))
    db_uri = app_cfg["database"]["uri"]
    db_type = "postgresql" if db_uri.startswith("postgres") else db_uri.split(":")[0]

    # since we can't run "lethbridge database upgrade head" here
    # without breaking tests, init the database directly via Alembic
    alembic_cfg = alembic.config.Config()
    alembic_cfg.set_main_option("script_location", "lethbridge:migrations")
    alembic_cfg.set_main_option("databases", db_type)
    alembic_cfg.set_section_option(db_type, "sqlalchemy.url", db_uri)
    alembic.command.upgrade(alembic_cfg, "head")

    yield mock_cmd_prefix


@mark.order("last")
@mark.parametrize(
    "mock_import_file_fixture, expected_systems",
    [
        param("mock_spansh_import", 6),
        param("mock_galaxy_data_file", 11, marks=mark.slow),
    ],
)
def test_cli_import_spansh(
    mock_cmd_prefix_initialized, mock_import_file_fixture, expected_systems, request
):
    mock_import_file = request.getfixturevalue(mock_import_file_fixture)
    result = runner.invoke(
        cli.app,
        ["-v"]
        + mock_cmd_prefix_initialized
        + ["import", "spansh", mock_import_file, "--foreground"],
    )
    assert result.exit_code == 0
    assert "IntegrityError" not in result.output

    # inspect mock database contents
    app_cfg = ConfigParser()
    app_cfg.read_file(open(mock_cmd_prefix_initialized[-1]))
    db_uri = app_cfg["database"]["uri"]
    engine = create_engine(db_uri, poolclass=NullPool)
    Session = sessionmaker(engine)
    with Session.begin() as session:
        stmt = select(func.count()).select_from(System)
        assert expected_systems == session.scalars(stmt).first()


@fixture
def mock_cmd_prefix_imported(mock_cmd_prefix_initialized, mock_spansh_import):
    # manually load "lethbridge.cli.import" since the name is
    # technically invalid lol
    cli_import = importlib.import_module("lethbridge.cli.import")
    import_spansh = getattr(cli_import, "spansh")

    # make a direct call to the Spansh import function since we know
    # it works per test_cli_import_spansh
    app_cfg = ConfigParser()
    app_cfg.read_file(open(mock_cmd_prefix_initialized[-1]))
    ctx = Context(TyperCommand("import_spansh"))
    ctx.obj = {"app_cfg": app_cfg}
    import_spansh(ctx=ctx, dataset=mock_spansh_import, foreground=True)

    yield mock_cmd_prefix_initialized


@mark.order("last")
@mark.parametrize(
    "mock_spansh_update_fixture",
    [
        param("mock_spansh_import_outdated"),
        param("mock_spansh_import_updated"),
    ],
)
def test_cli_import_spansh_update(
    mock_cmd_prefix_imported, mock_spansh_update_fixture, request
):
    # cache the last update time of the first test system
    app_cfg = ConfigParser()
    app_cfg.read_file(open(mock_cmd_prefix_imported[-1]))
    db_uri = app_cfg["database"]["uri"]
    engine = create_engine(db_uri, poolclass=NullPool)
    Session = sessionmaker(engine)
    with Session.begin() as session:
        test_system_1 = session.get(System, 1)
        old_date = test_system_1.date

    mock_spansh_update = request.getfixturevalue(mock_spansh_update_fixture)
    result = runner.invoke(
        cli.app,
        ["-v"]
        + mock_cmd_prefix_imported
        + ["import", "spansh", mock_spansh_update, "--foreground"],
    )
    assert result.exit_code == 0

    # inspect mock database contents
    with Session.begin() as session:
        test_system_1 = session.get(System, 1)
        assert old_date <= test_system_1.date
