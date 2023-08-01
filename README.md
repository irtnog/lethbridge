# lethbridge

[Free/libre/open source](LICENSE) client for the [Elite Dangerous Data Network](https://github.com/EDCD/EDDN) (and more)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<details>

<summary>The following is <strong>UNDER CONSTRUCTION</strong> and only reflects the intentions of the authors.</summary>

## Quickstart

1. Install [Docker Engine](https://docs.docker.com/engine/).  See below for host storage requirements.

2. Download and unpack the [latest release](../../releases/latest) of Lethbridge's Docker Compose project (e.g., `lethbridge-1.0.0-compose.zip`).

3. Review the contents of [.env.example](.env.example).  Save any changes to a file named `.env`.

4. Initialize the database and start the [EDDN](https://github.com/EDCD/EDDN) listener in the background with `docker compose start`.

Container images for the most recent Lethbridge major release get rebuilt weekly.  Download updated images by running `docker compose pull`.  Deploy them with `docker compose up -d`.  To remove cached copies of outdated images, run `docker image prune -f`.  The Lethbridge [CLI](https://en.wikipedia.org/wiki/Command-line_interface) can be accessed using `docker compose exec service`.  For more information, refer to the [Docker Compose documentation](https://docs.docker.com/compose/).

Lethbridge can import data from several sources.  Import jobs will run in background threads by default.  For example:

- To import galaxy map data from Spansh, use `lethbridge import spansh galaxy`.

- To import Guardian points of interest from Canonn, use `lethbridge import canonn guardians`.

- To import Thargoid surface sites from edtools.cc, use `lethbridge import edtools "Active Thargoid Structures"`.

For more information, run `lethbridge import --help`.

## Theory of Operation

The [Elite Dangerous Data Network (EDDN)](https://github.com/EDCD/EDDN) is...

Named after famed explorer CMDR Qohen Leth, Lethbridge connects to the EDDN and listens...

See ["Supported Databases" in the SQLAlchemy documentation](https://docs.sqlalchemy.org/latest/core/engines.html#supported-databases)...

### Resource Planning

The Spansh galaxy data dump requires... of disk space...

EDDN generates about... of network traffic...

### Backup/Restore

Continuous archiving and point-in-time recovery (PITR)...

https://www.postgresql.org/docs/current/backup.html

https://duckduckgo.com/?q=docker+postgresql+wal+archiving

https://stackoverflow.com/questions/67442236/setting-up-wal-archiving-by-passing-archive-command-on-the-postgres-command-line

https://www.digitalocean.com/community/tutorials/how-to-set-up-continuous-archiving-and-perform-point-in-time-recovery-with-postgresql-12-on-ubuntu-20-04

https://stackoverflow.com/questions/56117363/postgres-backup-with-wal

https://www.postgresql.org/docs/current/continuous-archiving.html

https://www.fusionbox.com/blog/detail/postgresql-wal-archiving-with-wal-g-and-s3-complete-walkthrough/644/

https://hub.docker.com/r/koehn/postgres-wal-g

https://github.com/abevoelker/docker-postgres

https://hub.docker.com/r/akcjademokracja/postgresql-wal-e/#!

### Troubleshooting

## Contributing

All Python code must match the [Black](https://black.readthedocs.io/) code style.  Follow [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) and [the Home Assistant YAML style guide](https://developers.home-assistant.io/docs/documenting/yaml-style-guide/) as appropriate.

In Git commit messages, follow the [Angular Commit Message Conventions](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit).  These scopes are currently active in this project:

- the top-level Python module name sans the `lethbridge.` prefix and any suffixes, e.g., `database` for `lethbridge.database`, `cli` for `lethbridge.cli.configure`

- `docker`

- `packaging`

- `changelog`

- `release`

### Development Environment

```
pip install -e .[dev]
```

https://setuptools.pypa.io/en/latest/userguide/development_mode.html

https://stackoverflow.com/questions/69711606/how-to-install-a-package-using-pip-in-editable-mode-with-pyproject-toml

https://pre-commit.com/

### Database Migrations Using Alembic

[Alembic](https://alembic.sqlalchemy.org/) is installed as part of the development environment documented above.

This project started with Alembic's multidb template.  The primary difference between that and the generic template is that multidb will run the migrations as many times as there are databases configured, providing one engine name and associated context for each run.  The migration will restrict what runs within it to just the appropriate migrations for that engine; cf. [the mako template](src/migrations/script.py.mako).  Adjust `databases` in [Alembic's configuration](alembic.ini) as necessary, with a `sqlalchemy.url` for each engine name, but **DO NOT** commit usernames or passwords as part of recorded changes to that file.

**Alembic commands MUST be run from the project root directory, i.e., the same directory as _alembic.ini_.**

To develop new database migrations:

1. Perform an editable installation of Lethbridge as documented in ["Development Environment"](#development-environment) above.

2. Deploy the test databases, e.g., PostgreSQL in a container.

3. Check the Alembic configuration by running `alembic current` from the project root directory.

4. Generate a new revision based on the current model by running `alembic revision --autogenerate -m "<summary>"`.  Revision summaries MUST follow the same conventions as Git commit message summaries, and one SHOULD use the same summary for both.

5. Reset the test databases by running `alembic downgrade base`.

6. Migrate the test databases to the latest model by running `alembic upgrade head`.

### Test Environment

```
pip install -e .[test]
pytest -s -v integration/
```

</details>
