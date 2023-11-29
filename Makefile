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

# Install Lethbridge in a virtual environment.  (See also the build-deps target.)

PYV = $(shell python3 -c "import sys;print('{}.{}'.format(*sys.version_info[:2]))")

dev-infra: .venv/lib/python$(PYV)/site-packages/psycopg2.py

.venv/lib/python$(PYV)/site-packages/psycopg2.py: lethbridge.egg-info
	echo "from psycopg2cffi import compat\ncompat.register()" > $@

lethbridge.egg-info: .venv pyproject.toml src/*.py src/*/*.py
	. .venv/bin/activate; pip install -U pip-with-requires-python
	. .venv/bin/activate; pip install -U pip setuptools
	. .venv/bin/activate; pip install -e .[psycopg2cffi,dev,test]

venv: .venv

.venv:
	python3 -m venv $@

smoke: dev-infra
	. .venv/bin/activate; pytest -m "smoke and not slow"

test tests: dev-infra
	. .venv/bin/activate; pytest

coverage: dev-infra
	. .venv/bin/activate; pytest --cov=lethbridge

dist: dev-infra
	. .venv/bin/activate; python -m build

distcheck: dist
	. .venv/bin/activate; twine check dist/*

distclean:
	rm -rf dist

# Install, run, or update pre-commit hooks.

pre-commit: .git/hooks/pre-commit

.git/hooks/pre-commit: .pre-commit-config.yaml dev-infra
	. .venv/bin/activate; pre-commit install --install-hooks

check checks lint: pre-commit
	. .venv/bin/activate; pre-commit validate-config
	. .venv/bin/activate; pre-commit validate-manifest
	. .venv/bin/activate; pre-commit run --show-diff-on-failure --all-files

# Install Lethbridge in a container image.

builder tester:
	docker build -t lethbridge:$@ --target $@ .

container docker:
	docker build -t lethbridge .

prune:
	docker system prune --all --volumes --force

# Launch databases for developing Alembic migrations

postgresql:
	docker run -d -p 127.0.0.1:5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust -e POSTGRES_DB=lethbridge postgres:14

# Install (or remove) build dependencies on Debian/Ubuntu.  Note that
# these targets must be invoked by root.  Also note that the
# purge-deps target can remove packages other that the ones listed
# here, so keep the confirmation prompts to avoid footguns.

DEBIAN_BUILD_DEPS = build-essential devscripts equivs postgresql
DEBIAN_INSTALL_TOOL = apt-get -o Debug::pkgProblemResolver=yes -y --no-install-recommends

build-deps: /etc/debian_version
ifneq ($(shell id -u), 0)
	@echo You must be root to perform this action.
	@exit 1
endif
	sed -i '/deb-src/s/^# //' /etc/apt/sources.list
	apt-get update
	$(DEBIAN_INSTALL_TOOL) install $(DEBIAN_BUILD_DEPS)
	mk-build-deps -i -r -t "$(DEBIAN_INSTALL_TOOL)" python3-psycopg2
	mk-build-deps -i -r -t "$(DEBIAN_INSTALL_TOOL)" python3-psycopg2cffi
	rm -f *.buildinfo *.changes

clean-deps: /etc/debian_version
ifneq ($(shell id -u), 0)
	@echo You must be root to perform this action.
	@exit 1
endif
	apt-mark auto $(DEBIAN_BUILD_DEPS) psycopg2-build-deps python-psycopg2cffi-build-deps
	apt-get autoremove

clean:
	rm -rf build .coverage dist lethbridge.egg-info .pytest_cache .venv*
	find . -type d -name __pycache__ -print | xargs rm -rf
