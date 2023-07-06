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
from . import DATABASE_ERROR
from . import SUCCESS
from datetime import datetime
from marshmallow import EXCLUDE
from marshmallow import post_dump
from marshmallow import post_load
from marshmallow import pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from psycopg2cffi import compat
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional
import logging

# configure module-level logging
logger = logging.getLogger(__name__)

# invoke psycopg2cffi compatibility hook
compat.register()


# tracks definitions and related metadata for the tables created below
class Base(DeclarativeBase):
    pass


class State(Base):
    """A faction's influence over and status within a given system.

    This models a faction's state in the background simulation (BGS)
    as a bi-directional association table in the SQLAlchemy ORM since
    BGS state must include data beyond the system/faction many-to-many
    relationship.

    """

    __tablename__ = "bgs_state"

    # foreign keys linking the two tables
    faction_name: Mapped[str] = mapped_column(
        ForeignKey("faction.name"),
        primary_key=True,
    )
    system_id64: Mapped[int] = mapped_column(
        ForeignKey("system.id64"),
        primary_key=True,
    )

    # extra data
    # TODO: happiness? not in Spansh dumps
    influence: Mapped[float]
    state: Mapped[str]

    # link this association to the corresponding ORM object via the
    # named attribute (and vice versa in the named ORM classes)
    faction: Mapped["Faction"] = relationship(back_populates="systems")
    system: Mapped["System"] = relationship(back_populates="factions")

    def __repr__(self):
        return (
            f"<BGS State({self.faction.name!r} in "
            + f"{(self.system or 'pending')!r}: "
            + f"{self.state}, influence={self.influence})>"
        )


class Faction(Base):
    """A minor faction, player or otherwise---as opposed to a Power,
    superpower, or species."""

    __tablename__ = "faction"

    # FIXME: create index column for factions? (why would one?)
    # id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(primary_key=True)
    allegiance: Mapped[str]
    government: Mapped[str]

    controlledSystems: Mapped[List["System"]] = relationship(
        back_populates="controllingFaction"
    )

    systems: Mapped[List["State"]] = relationship(back_populates="faction")

    def __repr__(self):
        return f"<Faction({self.name!r})>"

    def __eq__(self, other: Faction) -> bool:
        return (
            self.name == other.name
            and self.allegiance == other.allegiance
            and self.government == other.government
        )


class System(Base):
    """A gravitationally bound group of stars, planets, and other
    bodies."""

    __tablename__ = "system"

    id64: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]  # not unique, e.g., AH Cancri
    x: Mapped[float]  # coords
    y: Mapped[float]
    z: Mapped[float]
    allegiance: Mapped[str | None]
    government: Mapped[str | None]
    primaryEconomy: Mapped[str | None]
    secondaryEconomy: Mapped[str | None]
    security: Mapped[str | None]
    population: Mapped[int | None] = mapped_column(BigInteger)
    bodyCount: Mapped[int | None]
    controllingFaction_id: Mapped[str | None] = mapped_column(
        ForeignKey("faction.name")
    )
    controllingFaction: Mapped[Optional["Faction"]] = relationship(
        back_populates="controlledSystems"
    )
    factions: Mapped[List["State"]] = relationship(back_populates="system")
    # powers
    powerState: Mapped[str | None]
    date: Mapped[datetime]
    # bodies
    # stations

    def __repr__(self):
        return f"<System(id64={self.id64!r}, {self.name!r})>"

    def __eq__(self, other: System) -> bool:
        return (
            self.id64 == other.id64
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
            # TODO
            # and self.controllingFaction == other.controllingFaction
            # and self.factions == other.factions
            # powers
            and self.powerState == other.powerState
            and self.date == other.date
            # bodies
            # stations
        )


class FactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Faction
        exclude = ["controlledSystems", "systems"]
        include_fk = True
        include_relationships = True
        load_instance = True


class StateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = State
        exclude = ["faction_name", "system_id64", "system"]
        include_fk = True
        include_relationships = True
        load_instance = True

    faction = Nested(FactionSchema)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        new_data = out_data.copy()

        # unwrap the faction data
        faction = new_data.pop("faction")
        new_data.update(faction)

        return new_data


class SystemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = System
        exclude = ["controllingFaction_id"]
        unknown = EXCLUDE
        include_fk = True
        include_relationships = True
        load_instance = True

    controllingFaction = Nested(FactionSchema, required=False, allow_none=True)
    factions = Nested(StateSchema, many=True, required=False)

    # TODO: translate between 'Anarchy'/'None' and None
    # TODO: powerState key denotes Bubble system?

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        new_data = out_data.copy()

        # wrap coords
        coords = {
            "x": new_data.pop("x"),
            "y": new_data.pop("y"),
            "z": new_data.pop("z"),
        }
        new_data["coords"] = coords

        # make a copy of the factions list sorted by faction name; cf.
        # https://docs.python.org/3/library/functions.html#sorted
        if new_data.get("factions"):
            new_data["factions"] = sorted(
                new_data["factions"], key=lambda faction: faction["name"]
            )

        # remove empty keys to save space
        optional_columns = [
            "allegiance",
            "government",
            "primaryEconomy",
            "secondaryEconomy",
            "security",
            "population",
            "bodyCount",
            "controllingFaction",
            "factions",
            "powerState",
        ]
        for k in optional_columns:
            if not new_data.get(k):
                try:
                    new_data.pop(k)
                except KeyError:
                    pass

        return new_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        new_data = in_data.copy()

        # unwrap coords
        coords = new_data.pop("coords")
        new_data.update(coords)

        new_data["factions"] = [
            {
                "faction": {
                    "name": f.get("name"),
                    "allegiance": f.get("allegiance"),
                    "government": f.get("government"),
                },
                "state": f.get("state"),
                "influence": f.get("influence"),
            }
            for f in new_data.get("factions", [])
        ]

        return new_data

    @post_load
    def post_process_input(self, in_data, **kwargs):
        # make sure we're being called after the System object was
        # created
        if not isinstance(in_data, System):
            return in_data

        # Replace the duplicate of the controllingFaction object in
        # the System's faction state list.  Otherwise, the ORM
        # generates a duplicate INSERT, which violates the Faction's
        # uniqueness constraint.  The ORM can't detect this, and
        # StateSchema (when creating factions) does not communicate
        # with FactionSchema (when creating controllingFaction).
        for bgs_state in in_data.factions:
            if bgs_state.faction == in_data.controllingFaction:
                bgs_state.faction = in_data.controllingFaction

        return in_data


def init_database(uri: str, force: bool = False) -> int:
    """Create tables, etc., in the database."""
    try:
        logger.debug("Creating engine.")
        engine = create_engine(uri)
        if force:
            logger.debug("Dropping existing tables, etc.")
            Base.metadata.drop_all(engine)
        logger.debug("Creating tables, etc.")
        Base.metadata.create_all(engine)
    except Exception as e:
        logger.info(e)
        return DATABASE_ERROR
    return SUCCESS
