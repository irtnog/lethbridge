# Contributing

This project combines [test-driven development](https://tdd.mooc.fi/) with the [Git feature branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).  Please submit your changes for review as a [GitHub pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests).  Changes must include functional and integration tests.

## Development Environment

This project requires Python 3.10 and Docker 20.10 (or newer).  To set up your development environment on Linux, run these commands from the project root directory:

- `sudo make build-deps`—installs build dependencies (Debian/Ubuntu only)

- `make`—creates (or updates) a virtual environment named `.venv` in the project root directory and performs an editable installation of this project plus development and testing tools

- `make pre-commit`—installs optional pre-commit hooks that require the virtual environment to be active in your code editor or [Git porcelain](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain)

- `. .venv/bin/activate` (Bourne shells), `source .venv/bin/activate.csh` (C shells), etc.—activates the virtual environment

Additional [make(1)](https://linux.die.net/man/1/make) targets are available, several of which are listed below.  Review the [Makefile](Makefile) for details.

- `make test`—performs comprehensive functional and integration testing of this project

- `make smoke`—runs a subset of the test suite (SQLite-only)

- `make docker`—builds a fully tested and release-ready container image

## Code Style

The following code styles are in use:

- [Python Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/)

- [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

- [the Home Assistant YAML style guide](https://developers.home-assistant.io/docs/documenting/yaml-style-guide/)

## Commit Messages

This project implements [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) using [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).  Please use English in commit messages.  The first line of the commit message should be at most 100 characters, while the rest of the commit message should be wrapped at column 70.  A commit's description should be a verb phrase in the imperative present tense, with the starting verb in lower case and no ending punctuation.

Valid commit types are:

- **build**—changes to the build system or external dependencies

- **ci**—changes to the CI configuration files and scripts

- **docs**—documentation-only changes

- **feat**—a new feature

- **fix**—a bug fix

- **perf**—a code change that improves performance

- **refactor**—a code change that neither fixes a bug nor adds a feature

- **test**—new tests or corrections to existing tests

A commit's scope should be the second-level Python module name sans the `lethbridge.` prefix or any suffixes with a few exceptions.  Valid commit scopes are:

- [lethbridge](src/__init__.py) and [main](src/__main__.py)—for the corresponding top-level dunder modules

- [cli](src/cli/)—the Lethbridge command line interface, using [Typer](https://typer.tiangolo.com/)

- [config](src/config.py)—the default configuration and related helper functions

- [database](src/database.py)—the data model, defined using [SQLAlchemy ORM](https://docs.sqlalchemy.org/latest/orm)

- [migrations](src/migrations/)—database schema migrations handled by [Alembic](https://alembic.sqlalchemy.org/)

- [schemas](src/schemas)—parsers for data imports and exports defined using [marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/)

- **packaging**—package layout or other metadata, e.g., the arrangement of [src/](src/), alterations to [pyproject.toml](pyproject.toml) or [Dockerfile](Dockerfile)

- no scope—for **refactor** or **test** changes covering multiple scopes; or for **build**, **ci**, or **doc** changes not specific to one scope

## Database Migrations

This project uses [Alembic](https://alembic.sqlalchemy.org/) to manage the database schema on supported [engines](https://docs.sqlalchemy.org/latest/core/engines.html) via the [multidb migration template](https://github.com/sqlalchemy/alembic/tree/main/alembic/templates/multidb).  **Alembic commands _MUST_ be run from the project root directory, i.e., the same directory as [alembic.ini](alembic.ini).**  For convenience's sake, the Makefile provides these targets:

- `make alembic-<COMMAND> ARGS="[ARGUMENT]..."`—a generic wrapper for Alembic commands, e.g., `make alembic-history ARGS="-v -i"`

- `make alembic-start` and `make alembic-stop`—creates or destroys databases for use by Alembic or other project development work

- `make alembic-backup` and `make alembic-restore`—dumps or loads data into the above databases

To develop a new database migration:

1. After modifying the data model, [generate a new schema revision](https://alembic.sqlalchemy.org/latest/autogenerate.html) with `make alembic-autogenerate MESSAGE="<revision summary>"`.  **WARNING: This command will delete any existing databases created by `make alembic-start`.**  Revision summaries should mirror the corresponding Git commit description, e.g., `address conflict with FDevIDs`.

2. Review the new schema revision.  Alembic cannot detect certain changes, e.g., renaming tables or column names, nor can it create data transformations.  The developer must handle these cases.  For more information, refer to ["What does Autogenerate Detect (and what does it not detect?)"](https://alembic.sqlalchemy.org/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect) in the Alembic documentation.

3. Create database dumps for integration testing from the [mock galaxy data](tests/mock-galaxy-data.json) with `make migration-test-fixtures`.  **WARNING: This command will delete any existing databases created by `make alembic-start`.**

4. Add the new revision to [the database migration tests](tests/test_cli_database.py).

To add support for a new database engine:

1. In the Alembic configuration file, [alembic.ini](alembic.ini), add the engine to the `databases` list in [alembic.ini](alembic.ini).  Add a section for that engine between the `[alembic]` and `[post_write_hooks]` sections.  In the new database section, specify a `sqlalchemy.url` for the engine.  **DO NOT** commit usernames or passwords as part of recorded changes to **alembic.ini**.

2. In the [Makefile](Makefile), add support for the new engine to the `alembic-%` target and the `generate-migration-test-fixture-target` macro.
