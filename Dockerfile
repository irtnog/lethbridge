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

# This container image definition uses a multi-stage build process;
# cf. https://pythonspeed.com/articles/multi-stage-docker-python/.
# This avoids creating extraneous layers with build or test artifacts,
# making the final image smaller.

# Default to this version of Python.  Override via a build argument.
ARG BASE_VERSION=3.11

# Start with an image based on the selected Python version.
FROM python:${BASE_VERSION} as base
ARG BASE_VERSION
ENV BASE_VERSION=${BASE_VERSION}
RUN set -eux; \
    groupadd -g 1000 lethbridge; \
    useradd -m -g 1000 -u 1000 lethbridge
ENV PATH=/home/lethbridge/.local/bin:$PATH
WORKDIR /home/lethbridge
# Drop root privileges to hinder container escapes.
USER lethbridge:lethbridge

# The first stage defines the build environment and includes
# everything needed to compile and install the project.
FROM base as builder
COPY LICENSE pyproject.toml .
COPY src src
RUN set -eux; \
    pip install .[psycopg2cffi]; \
    echo "from psycopg2cffi import compat\ncompat.register()" \
    > /home/lethbridge/.local/lib/python${BASE_VERSION}/site-packages/psycopg2.py

# The second stage defines the test environment and verifies the
# software installed in the first stage.
FROM builder as tester
USER root
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends postgresql
USER lethbridge:lethbridge
ENV VIRTUAL_ENV=/home/lethbridge/.venv
ENV PATH=$VIRUAL_ENV/bin:$PATH
COPY tests tests
RUN set -eux; \
    python -m venv --system-site-packages .venv; \
    pip install --user .[test]; \
    pytest --cov=lethbridge --report-log=pytest.out

# The third stage defines the released container image and should only
# include what's required to run the software in production to hinder
# pivoting.
FROM base
# Re-installing runs the risk of installing a different version of a
# dependency, which invalidates the test results.
COPY --from=builder /home/lethbridge/.local /home/lethbridge/.local
# Include the test report as a kind of airworthiness certificate.
COPY --from=tester /home/lethbridge/pytest.out .
COPY --chown=root:root --chmod=755 docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["lethbridge","listen"]
