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
from marshmallow import post_dump
from marshmallow import pre_load
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
    x: Mapped[float]            # coords
    y: Mapped[float]
    z: Mapped[float]
    allegiance: Mapped[Optional[str]]
    government: Mapped[str] = mapped_column(default='None')
    primaryEconomy: Mapped[str] = mapped_column(default='None')
    secondaryEconomy: Mapped[str] = mapped_column(default='None')
    security: Mapped[str] = mapped_column(default='Anarchy')
    population: Mapped[int] = mapped_column(default=0)
    bodyCount: Mapped[int] = mapped_column(default=0)
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
        return (
            isinstance(other, System)
            and self.id64 == other.id64
            and self.name == other.name
            and self.x == other.x  # coords
            and self.y == other.y
            and self.z == other.z
            and self.allegiance == other.allegiance
            and self.government == other.government
            and self.primaryEconomy == other.primaryEconomy
            and self.secondaryEconomy == other.secondaryEconomy
            and self.security == other.security
            and self.population == other.population
            and self.bodyCount == other.bodyCount
            # controllingFaction
            # factions
            # powers
            and self.powerState == other.powerState
            and self.date == other.date
            # bodies
            # stations
        )


class SystemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = System
        unknown = EXCLUDE
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def wrap_coords(self, out_data, **kwargs):
        coords = {
            'x': out_data.pop('x'),
            'y': out_data.pop('y'),
            'z': out_data.pop('z'),
        }
        out_data['coords'] = coords
        return out_data

    @pre_load
    def flatten_coords(self, in_data, **kwargs):
        coords = in_data.pop('coords')
        in_data.update(coords)
        return in_data
