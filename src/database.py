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


class Base(DeclarativeBase):
    """This class tracks ORM class definitions and related metadata
    for the tables created in this module."""

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
            f"<BGS State({self.faction!r} in "
            + f"{(self.system or 'pending')!r}: "
            + f"{self.state}, influence={self.influence})>"
        )

    def __eq__(self, other: State) -> bool:
        # don't check back-populated columns since that would lead to
        # an infinite loop
        return (
            self.faction_name == other.faction_name
            and self.system_id64 == other.system_id64
            and self.influence == other.influence
            and self.state == other.state
        )


class Faction(Base):
    """A minor faction, player or otherwise---as opposed to a Power,
    superpower, or species.

    Note that fleet carriers, being stations, are controlled by a
    virtual faction named FleetCarrier.  This faction has neither
    allegiance nor government."""

    __tablename__ = "faction"

    name: Mapped[str] = mapped_column(primary_key=True)
    allegiance: Mapped[str | None]
    government: Mapped[str | None]

    controlledSystems: Mapped[List["System"]] = relationship(
        back_populates="controllingFaction"
    )
    controlledStations: Mapped[List["Station"]] = relationship(
        back_populates="controllingFaction"
    )

    systems: Mapped[List["State"]] = relationship(back_populates="faction")

    def __repr__(self):
        return f"<Faction({self.name!r})>"

    def __eq__(self, other: Faction) -> bool:
        return self.name == other.name


class PowerPlay(Base):
    """A Power's influence over a given system.

    This models a Power's state in the background simulation (BGS) as
    a bi-directional association table in the SQLAlchemy ORM since
    that state might include data beyond the system/Power many-to-many
    relationship.

    """

    __tablename__ = "powerplay"

    # foreign keys linking the two tables
    power_name: Mapped[str] = mapped_column(
        ForeignKey("power.name"),
        primary_key=True,
    )
    system_id64: Mapped[int] = mapped_column(
        ForeignKey("system.id64"),
        primary_key=True,
    )

    # TODO: extra data?  Find out how PowerPlay data gets collected.
    # Is it available via the game journal, or do players scrape it
    # manually from the game UI?  (It's probably the latter.)

    # link this association to the corresponding ORM object via the
    # named attribute (and vice versa in the named ORM classes)
    power: Mapped["Power"] = relationship(back_populates="systems")
    system: Mapped["System"] = relationship(back_populates="powers")

    def __repr__(self):
        return f"<PowerPlay({self.power!r} in " + f"{(self.system or 'pending')!r})>"

    def __eq__(self, other: PowerPlay) -> bool:
        # don't check back-populated columns since that would lead to
        # an infinite loop
        return (
            self.power_name == other.power_name
            and self.system_id64 == other.system_id64
        )


class Power(Base):
    """Individuals and organization who wield greater influence over
    the galactic polity than minor factions but less than a
    superpower."""

    __tablename__ = "power"

    name: Mapped[str] = mapped_column(primary_key=True)

    systems: Mapped[List["PowerPlay"]] = relationship(back_populates="power")

    def __repr__(self):
        return f"<Power({self.name!r})>"

    def __eq__(self, other: Power) -> bool:
        # don't check back-populated columns since that would lead to
        # an infinite loop
        return self.name == other.name


class StationService(Base):
    """What services a station provides, modeled as a one-to-many
    relationship."""

    __tablename__ = "station_service"

    service: Mapped[str] = mapped_column(primary_key=True)
    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"), primary_key=True)


class Station(Base):
    """A space station, mega ship, fleet carrier, surface port, or
    settlement.  Fleet carriers and mega ships are mobile."""

    __tablename__ = "station"

    name: Mapped[str]
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    updateTime: Mapped[datetime]
    controllingFaction_id: Mapped[str | None] = mapped_column(
        ForeignKey("faction.name")
    )
    controllingFaction: Mapped[Optional["Faction"]] = relationship(
        back_populates="controlledStations"
    )
    controllingFactionState: Mapped[str | None]
    distanceToArrival: Mapped[float | None]
    primaryEconomy: Mapped[str | None]
    # economies
    allegiance: Mapped[str | None]  # matches controllingFaction?
    government: Mapped[str | None]  # matches controllingFaction?
    services: Mapped[List["StationService"]] = relationship()
    type: Mapped[str | None]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    largeLandingPads: Mapped[int | None]  # landingPads
    mediumLandingPads: Mapped[int | None]
    smallLandingPads: Mapped[int | None]
    # market
    # shipyard
    # outfitting

    # a system may contain many space stations; model this as a
    # bi-directional, nullable, many-to-one relationship
    # (stations:system)
    system_id64: Mapped[Optional[int]] = mapped_column(ForeignKey("system.id64"))
    system: Mapped[Optional["System"]] = relationship(back_populates="stations")

    # TODO: a body might support many surface ports...

    def __repr__(self):
        return f"<Station({self.name} in {(self.system or 'pending')!r})>"

    def __eq__(self, other: Station) -> bool:
        return self.id == other.id


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
    powers: Mapped[List["PowerPlay"]] = relationship(back_populates="system")
    powerState: Mapped[str | None]
    date: Mapped[datetime]
    # bodies
    stations: Mapped[List["Station"]] = relationship(back_populates="system")

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
            and self.controllingFaction == other.controllingFaction
            and self.factions == other.factions
            and self.powers == other.powers
            and self.powerState == other.powerState
            and self.date == other.date
            # bodies
            and self.stations == other.stations
        )


class FactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Faction
        exclude = ["controlledSystems", "controlledStations", "systems"]
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


class PowerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Power
        exclude = ["systems"]
        unknown = EXCLUDE
        include_fk = True
        include_relationships = True
        load_instance = True


class PowerPlaySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PowerPlay
        exclude = ["power_name", "system_id64", "system"]
        include_fk = True
        include_relationships = True
        load_instance = True

    power = Nested(PowerSchema)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return out_data.get("power", {}).get("name")


class StationServiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StationService
        exclude = ["station_id"]
        include_fk = True
        include_relationships = True
        load_instance = True


class StationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Station
        exclude = ["controllingFaction_id", "system_id64", "system"]
        unknown = EXCLUDE  # FIXME
        include_fk = True
        include_relationships = True
        load_instance = True

    controllingFaction = Nested(FactionSchema, required=False, allow_none=True)
    services = Nested(StationServiceSchema, many=True, required=False)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        new_data = out_data.copy()

        # convert 0.0 to 0
        float_columns = [
            "distanceToArrival",
        ]
        for k in float_columns:
            if k in new_data and new_data[k] == 0.0:
                new_data[k] = 0

        # remove empty keys to save space
        required_columns = ["name", "id", "updateTime"]
        for k in set(new_data.keys()) - set(required_columns):
            if new_data.get(k) is None or new_data.get(k) == []:
                new_data.pop(k)

        # flatten controllingFaction
        if "controllingFaction" in new_data:
            controlling_faction = new_data.get("controllingFaction", {})
            new_data["controllingFaction"] = controlling_faction.get("name")
            if "controllingFactionState" not in new_data:
                # FIXME: why does Spansh do this?
                new_data["controllingFactionState"] = None

        # flatten services
        if "services" in new_data:
            new_data["services"] = [service["name"] for service in new_data["services"]]

        # wrap landingPads
        landingPads = {}
        for k_new, k_orig in [
            ("large", "largeLandingPads"),
            ("medium", "mediumLandingPads"),
            ("small", "smallLandingPads"),
        ]:
            if k_orig in new_data:
                landingPads[k_new] = new_data.pop(k_orig)
        if landingPads:
            new_data["landingPads"] = landingPads

        return new_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        new_data = in_data.copy()

        # wrap faction data but do not remove the station-level
        # allegiance and government attributes
        if "controllingFaction" in new_data:
            new_data["controllingFaction"] = {
                "name": new_data.get("controllingFaction"),
                "allegiance": new_data.get("allegiance"),
                "government": new_data.get("government"),
            }

        # wrap services
        if "services" in new_data:
            new_data["services"] = [
                {"service": service} for service in new_data.get("services", [])
            ]

        # flatten landingPads
        landingPads = new_data.pop("landingPads", {})
        if landingPads:
            new_data["largeLandingPads"] = landingPads.get("large")
            new_data["mediumLandingPads"] = landingPads.get("medium")
            new_data["smallLandingPads"] = landingPads.get("small")

        return new_data


class SystemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = System
        exclude = ["controllingFaction_id"]
        unknown = EXCLUDE  # FIXME
        include_fk = True
        include_relationships = True
        load_instance = True

    controllingFaction = Nested(FactionSchema, required=False, allow_none=True)
    factions = Nested(StateSchema, many=True, required=False)
    powers = Nested(PowerPlaySchema, many=True, required=False)
    # bodies
    stations = Nested(StationSchema, many=True, required=False)

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

        # remove empty keys to save space
        required_columns = ["id64", "name", "coords", "date", "bodies", "stations"]
        for k in set(new_data.keys()) - set(required_columns):
            if new_data.get(k) is None or new_data.get(k) == []:
                new_data.pop(k)

        # make a copy of the factions list sorted by faction name; cf.
        # https://docs.python.org/3/library/functions.html#sorted
        if "factions" in new_data:
            new_data["factions"] = sorted(
                new_data["factions"], key=lambda faction: faction["name"]
            )

        # make a sorted copy of the powers list
        if "powers" in new_data:
            new_data["powers"] = sorted(new_data["powers"])

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

        # restructure factions and powers lists to match ORM
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
        new_data["powers"] = [
            {"power": {"name": power}} for power in new_data.get("powers", [])
        ]

        return new_data

    @post_load
    def post_process_input(self, in_data, **kwargs):
        # make sure we're being called after the System object was
        # created
        if not isinstance(in_data, System):
            return in_data

        # index the faction list to facilitate deduplication
        _factions = {fs.faction.name: fs.faction for fs in in_data.factions}

        # replace duplicate controllingFaction objects (which the ORM
        # cannot detect, leading to uniqueness constraint violations
        # due to duplicate INSERT statements)
        if in_data.controllingFaction:
            _cfac = in_data.controllingFaction
            in_data.controllingFaction = _factions[_cfac.name]
        for station in in_data.stations:
            _cfac = station.controllingFaction
            if _cfac:  # not all stations have a controlling faction
                if _cfac.name in _factions:
                    station.controllingFaction = _factions[_cfac.name]
                else:
                    # add novel factions to the index, e.g., FleetCarrier
                    _factions[_cfac.name] = _cfac

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
