# Contributing

This project uses the [Git feature branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).  Please submit your changes for review as a [GitHub pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests).

## Development Environment

This project requires Python 3.10 or newer.  To set up your development environment on Linux, run these commands from the project root directory:

- `sudo make build-deps`—installs build dependencies (Debian/Ubuntu only)

- `make`—creates a virtual environment named `.venv` in the current working directory and performs an editable installation of this project, including development and testing tools

- `make pre-commit`—installs pre-commit hooks (requires the virtual environment to be active in your code editor or [Git porcelain](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain))

- `make test`—performs comprehensive functional and integration testing of this project

- `make smoke`—runs a shorter, faster subset of the test suite

- `make docker`—builds a fully tested and release-ready container image

Additional [make(1)](https://linux.die.net/man/1/make) targets are available.  Review the [Makefile](Makefile) for details.

## Code Style

The following code styles are in use:

- [Python Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/)

- [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

- [the Home Assistant YAML style guide](https://developers.home-assistant.io/docs/documenting/yaml-style-guide/)

## Commit Messages

This project implements [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) using [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).  Valid commit types are:

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

- no scope—for **refactor** or **test** changes covering multiple packages; or for **build**, **ci**, or **doc** changes not specific to one package

## Database Migrations

This project uses [Alembic](https://alembic.sqlalchemy.org/) to manage the database schema.  This project started with Alembic's multidb template.  Unlike Alembic's generic template, multidb will run migrations as many times as there are databases configured, providing one engine name and associated context for each run.  The migration will restrict what runs within it to just the appropriate migrations for that engine; cf. [the mako template](src/migrations/script.py.mako).

**Alembic commands _MUST_ be run from the project root directory, i.e., the same directory as [alembic.ini](alembic.ini).**

To develop new database migrations:

1. Perform an editable installation of this project as documented in [Development Environment](#development-environment) above.

2. Deploy the test databases, e.g., start PostgreSQL in a container.

3. Check the Alembic configuration by running `alembic current` from the project root directory.

4. Generate a new revision based on the current model by running `alembic revision --autogenerate -m "<summary>"`.  Revision summaries MUST follow the same conventions as Git commit message summaries, and one SHOULD use the same summary for both.

5. Reset the test databases by running `alembic downgrade base`.

6. Migrate the test databases to the latest model by running `alembic upgrade head`.

To add support for a new database engine:

1. Add the engine to the `databases` list in [alembic.ini](alembic.ini).  Please sort this list in alphabetical order.

2. Add a section for that engine between the `[alembic]` and `[post_write_hooks]` sections.  Please also keep the database sections in alphabetical order.

3. In the new database section, specify a `sqlalchemy.url` for the engine.  **DO NOT** commit usernames or passwords as part of recorded changes to **alembic.ini**.
