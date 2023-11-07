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

lethbridge.egg-info: .venv
	. .venv/bin/activate; pip install -e .[dev,test]

.venv:
	python3 -m venv --system-site-packages $@

test: lethbridge.egg-info
	. .venv/bin/activate; pytest

coverage: lethbridge.egg-info
	. .venv/bin/activate; pytest --cov=lethbridge

clean:
	rm -rf .coverage lethbridge.egg-info .pytest_cache .venv*
	find . -type d -name __pycache__ -print | xargs rm -rf

container:
	docker build -t lethbridge .

docker: container
