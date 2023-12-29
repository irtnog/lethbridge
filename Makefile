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

.PHONY: dev-infra venv debug run smoke test tests tests coverage dist \
	distcheck distclean pre-commit check checks list builder \
	tester container docker prune bashbrew manifest-tool \
	wait-until alembic-% migration-test-fixtures \
	build-deps clean-deps clean

# Install Lethbridge in a virtual environment.  (See also the
# build-deps target.)

PYTHON_VERSION := $(shell python3 -c "import sys;print('{}.{}'.format(*sys.version_info[:2]))")
PSYCOPG2CFFI_COMPAT := .venv/lib/python$(PYTHON_VERSION)/site-packages/psycopg2.py
DEVELOPMENT_INFRASTRUCTURE := \
	$(PSYCOPG2CFFI_COMPAT) \
	.venv/bin/bashbrew \
	.venv/bin/manifest-tool \
	.venv/bin/wait-until

dev-infra: $(DEVELOPMENT_INFRASTRUCTURE)

$(PSYCOPG2CFFI_COMPAT): lethbridge.egg-info
	echo "from psycopg2cffi import compat\ncompat.register()" > $@

lethbridge.egg-info: .venv pyproject.toml src/*.py src/*/*.py
	. .venv/bin/activate; pip install -U pip-with-requires-python
	. .venv/bin/activate; pip install -U pip setuptools
	. .venv/bin/activate; pip install -e .[psycopg2cffi,dev,test]

venv: .venv

.venv:
	python3 -m venv $@

smoke: | $(PSYCOPG2CFFI_COMPAT)
	. .venv/bin/activate; pytest -m "smoke and not slow"

test tests: | $(PSYCOPG2CFFI_COMPAT)
	. .venv/bin/activate; pytest $(ARGS)

coverage: | $(PSYCOPG2CFFI_COMPAT)
	. .venv/bin/activate; pytest --cov=lethbridge

dist: | $(PSYCOPG2CFFI_COMPAT)
	. .venv/bin/activate; python -m build

distcheck: | dist
	. .venv/bin/activate; twine check dist/*

distclean:
	rm -rf dist

# Install, run, or update pre-commit hooks.

pre-commit: .git/hooks/pre-commit

.git/hooks/pre-commit: .pre-commit-config.yaml | $(PSYCOPG2CFFI_COMPAT)
	. .venv/bin/activate; pre-commit install --install-hooks

check checks lint: .git/hooks/pre-commit
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

bashbrew: .venv/bin/bashbrew

.venv/bin/bashbrew: | .venv
# cf. https://stackoverflow.com/a/40119933
	$(eval TMP := $(shell mktemp -d))
	git clone --depth=1 https://github.com/docker-library/bashbrew $(TMP)
	cd $(TMP); go mod download
	cd $(TMP); ./bashbrew.sh --version
	cp $(TMP)/bin/bashbrew $@
	rm -rf $(TMP)

manifest-tool: .venv/bin/manifest-tool

.venv/bin/manifest-tool: | .venv
	$(eval TMP := $(shell mktemp -d))
	git clone --depth=1 https://github.com/estesp/manifest-tool $(TMP)
	cd $(TMP); make binary
	cp $(TMP)/manifest-tool $@
	rm -rf $(TMP)

wait-until: .venv/bin/wait-until

.venv/bin/wait-until: | .venv
	curl -L https://raw.githubusercontent.com/nickjj/wait-until/v0.3.0/wait-until -o $@
	chmod +x $@

# Manage the database schema.  Note that for SQLite, `alembic-restore`
# simulates a database DROP, similar to the PostgreSQL restore script.
# For further instructions, review CONTRIBUTING.md#database-migrations.

alembic-%: | $(PSYCOPG2CFFI_COMPAT) .venv/bin/wait-until
	$(eval alembic = . .venv/bin/activate; alembic)
	$(eval alembic_cmd = $(word 2, $(subst -, ,$@)))
	$(eval is_autogenerate_cmd = $(filter autogenerate, $(alembic_cmd)))
	$(eval is_backup_cmd = $(filter backup, $(alembic_cmd)))
	$(eval is_restore_cmd = $(filter restore, $(alembic_cmd)))
	$(eval is_start_cmd = $(filter start, $(alembic_cmd)))
	$(eval is_stop_cmd = $(filter stop, $(alembic_cmd)))
	$(eval has_no_message = $(if $(MESSAGE),,true))
	$(if $(and $(is_autogenerate_cmd),$(has_no_message)), \
		@echo Provide a revision summary via the MESSAGE variable\; e.g.:; \
		echo "    make" $@ 'MESSAGE="revised something"'; \
		exit 1 \
	)
	$(if $(is_autogenerate_cmd), \
		$(eval alembic_cmd = revision --autogenerate -m "$(MESSAGE)") \
	)
	$(eval is_alembic_cmd = $(filter-out backup restore start stop, $(alembic_cmd)))
	$(if $(or $(is_autogenerate_cmd),$(is_start_cmd)), \
		docker stop alembic-postgresql; \
		docker rm alembic-postgresql; \
		docker run -d --name alembic-postgresql \
			-p 127.0.0.1:5432:5432 \
			-e POSTGRES_HOST_AUTH_METHOD=trust \
			-e POSTGRES_DB=lethbridge \
			postgres:14; \
		. .venv/bin/activate; wait-until  \
			"docker exec alembic-postgresql psql -U postgres lethbridge -c 'select 1'"; \
		rm -f db.sqlite3; \
		$(alembic) upgrade head \
	)
	$(if $(is_alembic_cmd), \
		-$(alembic) $(alembic_cmd) $(ARGS), \
	$(if $(is_backup_cmd), \
		docker exec -t alembic-postgresql pg_dump -c -U postgres lethbridge > db.postgresql.bak; \
		sqlite3 db.sqlite3 .dump > db.sqlite3.bak, \
	$(if $(is_restore_cmd), \
		docker exec -i alembic-postgresql psql -U postgres postgres < db.postgresql.bak; \
		rm -f db.sqlite3; \
		touch db.sqlite3; \
		sqlite3 db.sqlite3 ".read db.sqlite3.bak", \
	)))
	$(if $(or $(is_autogenerate_cmd),$(is_stop_cmd)), \
		docker stop alembic-postgresql; \
		docker rm alembic-postgresql; \
		rm -f db.sqlite3 \
	)

# Generate database migration test fixture targets.  Please note the
# following:
#
# - In the multi-line variable definition, the use of late binding
#   with conditional functions forces re-evaluation of those
#   expressions every time the subsequent foreach functions call the
#   macro.
#
# - awk's PRNG gets seeded with the previous result because
#   consecutive invocations of rand() within short timeframes return
#   the same value!
#
# - Only run migration test fixture targets if they don't already
#   exist; cf. order-only pre-requisites
#   (https://www.gnu.org/software/make/manual/make.html#Prerequisite-Types).

tests/migration-fixtures:
	mkdir -p $@

define generate-migration-test-fixture-target
$(eval database = $1)
$(eval migration = $2)
$(eval revision = $(word 1, $(subst _, , $(notdir $(basename $(migration))))))
$(eval fixture = tests/migration-fixtures/$(database)-$(revision).sql)
$(eval tmpdir = $(or $(shell mktemp -d)))
$(eval is_postgresql = $(filter postgresql, $(database)))
$(eval port = $(or $(shell awk -v seed=$(port) \
	'BEGIN{srand(seed);print int(rand()*(65535-41952+1))+41952}' \
)))
$(eval lethbridge = . .venv/bin/activate; lethbridge -f $(tmpdir)/lethbridge.conf)
$(eval MIGRATION_TEST_FIXTURES += $(fixture))
$(fixture): | $(migration) $(PSYCOPG2CFFI_COMPAT) tests/migration-fixtures
	$(if $(is_postgresql), \
		docker stop alembic-postgresql; \
		docker rm alembic-postgresql; \
		docker run -d --name alembic-postgresql \
			-p 127.0.0.1:$(port):5432 \
			-e POSTGRES_HOST_AUTH_METHOD=trust \
			-e POSTGRES_DB=lethbridge \
			postgres:14; \
		. .venv/bin/activate; wait-until \
			"docker exec alembic-postgresql psql -U postgres lethbridge -c 'select 1'" \
	)
	$(lethbridge) configure set database uri \
		$(if $(is_postgresql), \
			"postgresql+psycopg2://postgres@localhost:$(port)/lethbridge?options=-c timezone=utc", \
			sqlite:///$(tmpdir)/galaxy.sqlite \
		)
	$(lethbridge) database upgrade $(revision)
	$(lethbridge) import spansh --fg tests/mock-galaxy-data.json
	$(if $(is_postgresql), \
		docker exec -t alembic-postgresql pg_dump -c -U postgres lethbridge > $(fixture), \
		sqlite3 $(tmpdir)/galaxy.sqlite .dump > $(fixture) \
	)
	$(if $(is_postgresql), \
		docker stop alembic-postgresql; \
		docker rm alembic-postgresql \
	)
	rm -rf $(tmpdir)
endef

$(foreach database, $(shell awk '/^databases = /{gsub(/,/,"",$$0);for(i=3;i<=NF;++i)print $$i}' alembic.ini), \
	$(foreach migration, $(wildcard src/migrations/versions/*.py), \
		$(eval $(call generate-migration-test-fixture-target,$(database),$(migration)))))

migration-test-fixtures: $(MIGRATION_TEST_FIXTURES)

# Install (or remove) build dependencies on Debian/Ubuntu.  Note that
# these targets must be invoked by root.

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
	$(DEBIAN_INSTALL_TOOL) install sqlite3
	rm -f *.buildinfo *.changes

clean-deps: /etc/debian_version
ifneq ($(shell id -u), 0)
	@echo You must be root to perform this action.
	@exit 1
endif
	apt-mark auto $(DEBIAN_BUILD_DEPS) psycopg2-build-deps python-psycopg2cffi-build-deps sqlite3
	apt-get autoremove

clean:
	rm -rf build .coverage dist lethbridge.egg-info .pytest_cache .venv*
	find . -type d -name __pycache__ -print | xargs rm -rf
