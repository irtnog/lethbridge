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
ENV VIRTUAL_ENV=/home/lethbridge/src/.venv
ENV PATH=$VIRUAL_ENV/bin:$PATH
RUN set -eux; \
    python -m venv --system-site-packages .venv; \
    pip install --user .[test]; \
    pytest --cov=lethbridge --report-log=/home/lethbridge/.local/pytest.out

FROM python:${PYTHON_VERSION}
RUN set -eux; \
    groupadd -g 1000 lethbridge; \
    useradd -m -g 1000 -u 1000 lethbridge
ENV PATH=/home/lethbridge/.local/bin:$PATH
COPY --from=builder /home/lethbridge/.local /home/lethbridge/.local
COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
WORKDIR /home/lethbridge
USER lethbridge:lethbridge
CMD ["lethbridge"]
