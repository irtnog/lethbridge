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

from __future__ import annotations
from datetime import datetime
from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional


# tracks definitions and related metadata for the tables created below
class Base(DeclarativeBase):
    pass


class System(Base):
    __tablename__ = 'system'

    id64: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]           # not unique, e.g., AH Cancri
    # coords
    allegiance: Mapped[Optional[str]]
    government: Mapped[Optional[str]]
    primaryEconomy: Mapped[Optional[str]]
    secondaryEconomy: Mapped[Optional[str]]
    security: Mapped[Optional[str]]
    population: Mapped[Optional[int]]
    bodyCount: Mapped[Optional[int]]
    # controllingFaction
    # factions
    # powers
    powerState: Mapped[Optional[str]]
    date: Mapped[datetime]
    # bodies
    # stations

    def __repr__(self):
        return f'<System(id64={self.id64!r}, {self.name!r})>'

    def __eq__(self, other):
        if not isinstance(other, System):
            return False
        if self.id64 != other.id64:
            return False
        if self.name != other.name:
            return False
        return True


class SystemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = System
        unknown = EXCLUDE
        include_fk = True
        include_relationships = True
        load_instance = True
