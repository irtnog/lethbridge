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

# Default to this version of Python.  Override via a build argument.
ARG PYTHON_VERSION=3.10

# This container image definition uses a multi-stage build process;
# cf. https://pythonspeed.com/articles/multi-stage-docker-python/.
# The first stage defines the build environment and should include
# everything needed to compile, install, and test the project.
FROM python:${PYTHON_VERSION} as builder
RUN set -eux; \
    groupadd -g 1000 lethbridge; \
    useradd -m -g 1000 -u 1000 lethbridge; \
    apt-get update; \
    apt-get install -y --no-install-recommends postgresql
ENV PATH=/home/lethbridge/.local/bin:$PATH
COPY --chown=lethbridge:lethbridge . /home/lethbridge/src
WORKDIR /home/lethbridge/src
USER lethbridge:lethbridge
RUN pip install --user .[psycopg2cffi]
COPY --chown=lethbridge:lethbridge <<EOF /home/lethbridge/.local/lib/python${PYTHON_VERSION}/site-packages/psycopg2.py
from psycopg2cffi import compat
compat.register()
EOF
# Prevent testing tools from cluttering up the release image by
# installing them into a virtual environment.
ENV VIRTUAL_ENV=/home/lethbridge/src/.venv
ENV PATH=$VIRUAL_ENV/bin:$PATH
RUN set -eux; \
    python -m venv --system-site-packages .venv; \
    pip install --user .[test]; \
# Store test results with the installation where they will be copied
# into the released container image as a kind of certification.
    pytest --cov=lethbridge --report-log=/home/lethbridge/.local/pytest.out

# The second stage defines the released container image and should
# only include what's required to run the software in production to
# hinder pivoting.
FROM python:${PYTHON_VERSION}
RUN set -eux; \
    groupadd -g 1000 lethbridge; \
    useradd -m -g 1000 -u 1000 lethbridge
ENV PATH=/home/lethbridge/.local/bin:$PATH
# Use the software installed and tested by the builder.
# (Re-installing runs the risk of installing a different version of a
# dependency, which invalidates the test results.)
COPY --from=builder /home/lethbridge/.local /home/lethbridge/.local
COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
WORKDIR /home/lethbridge
# Drop root privileges in production to hinder container escapes.
USER lethbridge:lethbridge
CMD ["lethbridge"]
