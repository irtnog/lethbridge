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
from os import environ
from pathlib import Path
from subprocess import run

from alembic.config import Config
from alembic.script import ScriptDirectory
from pytest import mark, param
from sqlalchemy import create_engine, make_url, text
from typer.testing import CliRunner

from lethbridge import cli

runner = CliRunner()


@mark.order("last")
@mark.parametrize(
    "revision",
    [
        param("head"),
        param("f6b71224e220", marks=mark.slow),
        param("a41aac16b9b4", marks=mark.slow),
        param("549d345a9779", marks=mark.slow),
    ],
)
def test_cli_database_upgrade(mock_cmd_prefix, revision, request):
    # note that mock_cmd_prefix is already parameterized via
    # mock_db_uri (cf. conftest.py), so grab the relevant configs and
    # adjust what would be parameters here on the fly
    app_cfg = ConfigParser()
    app_cfg.read_file(open(mock_cmd_prefix[-1]))
    db_uri = make_url(app_cfg["database"]["uri"])
    db_type = db_uri.get_backend_name()

    # select and load a backup, if one exists for this engine/revision
    db_backup = (
        Path(__file__).parent / "migration-fixtures" / f"{db_type}-{revision}.sql"
    )
    if db_backup.exists():
        match db_type:
            case "postgresql":
                psql_env = dict(environ)  # copy parent environment
                psql_env["PGPASSWORD"] = db_uri.password
                psql_uri = "postgresql://%(user)s@%(host)s:%(port)s/postgres" % {
                    "user": db_uri.username,
                    "host": db_uri.host,
                    "port": db_uri.port or 5432,
                }
                run(
                    ["psql", "-f", str(db_backup), psql_uri],
                    env=psql_env,
                    check=True,
                )
            case "sqlite":
                Path(db_uri.database).touch()
                run(
                    ["sqlite3", db_uri.database, f".read {str(db_backup)}"],
                    check=True,
                )

    # run the migration (which is just a wrapper for Alembic)
    result = runner.invoke(cli.app, mock_cmd_prefix + ["database", "upgrade", "head"])
    assert result.exit_code == 0

    # ask Alembic for the latest schema revision
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "lethbridge:migrations")
    alembic_script = ScriptDirectory.from_config(alembic_cfg)
    head_revision = alembic_script.get_current_head()

    # verify the upgrade succeeded
    engine = create_engine(db_uri)
    with engine.connect() as conn:
        result = conn.execute(text("select version_num from alembic_version"))
        assert head_revision == result.scalar_one()
