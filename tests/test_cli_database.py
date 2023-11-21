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

from alembic.config import Config
from alembic.script import ScriptDirectory
from pytest import mark
from sqlalchemy import create_engine, text
from typer.testing import CliRunner

from lethbridge import cli

runner = CliRunner()


@mark.order("last")
def test_cli_database_upgrade(mock_cmd_prefix):
    result = runner.invoke(cli.app, mock_cmd_prefix + ["database", "upgrade", "head"])
    assert result.exit_code == 0

    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "lethbridge:migrations")
    alembic_script = ScriptDirectory.from_config(alembic_cfg)
    head_revision = alembic_script.get_current_head()

    lethbridge_cfg = ConfigParser()
    lethbridge_cfg.read_file(open(mock_cmd_prefix[-1]))
    engine = create_engine(lethbridge_cfg["database"]["uri"])
    with engine.connect() as conn:
        result = conn.execute(text("select version_num from alembic_version"))
        assert head_revision == result.scalar_one()
