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
from collections import ChainMap
from datetime import datetime
from marshmallow import EXCLUDE
from marshmallow import post_dump
from marshmallow import post_load
from marshmallow import pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
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


class Base(DeclarativeBase):
    """This class tracks ORM class definitions and related metadata
    for the tables created in this module."""

    pass


class FactionState(Base):
    """A faction's influence over and status within a given system.

    This models a faction's state in the background simulation as a
    bi-directional association table in the SQLAlchemy ORM since this
    state includes data beyond the system/faction many-to-many
    relationship."""

    __tablename__ = "faction_state"

    # TODO: happiness? not in Spansh dumps
    influence: Mapped[float]
    state: Mapped[str]

    # link this association table to the corresponding ORM objects via
    # the named attribute (and vice versa in the named ORM classes)
    faction_name: Mapped[str] = mapped_column(
        ForeignKey("faction.name"),
        primary_key=True,
    )
    faction: Mapped["Faction"] = relationship(back_populates="systems")
    system_id64: Mapped[int] = mapped_column(
        ForeignKey("system.id64"),
        primary_key=True,
    )
    system: Mapped["System"] = relationship(back_populates="factions")

    def __repr__(self):
        return (
            f"<FactionState({self.influence}/{self.state}, "
            + f"faction_name={self.faction_name}, "
            + f"system_id64={self.system_id64})>"
        )

    def __eq__(self, other: FactionState) -> bool:
        # don't check back-populated columns since that would lead to
        # an infinite loop
        return (
            self.faction_name == other.faction_name
            and self.system_id64 == other.system_id64
            and self.influence == other.influence
            and self.state == other.state
        )


class Faction(Base):
    """A minor faction, player or otherwise---as opposed to a major
    power, superpower, or species.

    Note that fleet carriers, being stations, are controlled by a
    virtual faction named FleetCarrier.  This faction has neither
    allegiance nor government."""

    __tablename__ = "faction"

    name: Mapped[str] = mapped_column(primary_key=True)
    allegiance: Mapped[str | None]
    government: Mapped[str | None]

    controlledStations: Mapped[List["Station"]] = relationship(
        back_populates="controllingFaction"
    )

    controlledSystems: Mapped[List["System"]] = relationship(
        back_populates="controllingFaction"
    )
    systems: Mapped[List["FactionState"]] = relationship(back_populates="faction")

    def __repr__(self):
        return f"<Faction({self.name!r})>"

    def __eq__(self, other: Faction) -> bool:
        return self.name == other.name


class PowerPlay(Base):
    """Major political powers are individuals and organization who
    wield greater influence over the galactic polity than minor
    factions but less than a superpower, modeled as a many-to-many
    relationship.

    This models a Power's influence over a given system in the
    background simulation (BGS) as a one-to-many relationship."""

    __tablename__ = "powerplay"

    power: Mapped[str] = mapped_column(primary_key=True)
    # TODO: additional data?  Find out how PowerPlay data gets
    # collected.  Is it available via the game journal, or do players
    # scrape it manually from the game UI?  (It's probably the
    # latter.)
    system_id64: Mapped[int] = mapped_column(
        ForeignKey("system.id64"),
        primary_key=True,
    )

    def __repr__(self):
        return f"<PowerPlay({self.power}, system_id64={self.system_id64}))>"

    def __eq__(self, other: PowerPlay) -> bool:
        return (
            self.power_name == other.power_name
            and self.system_id64 == other.system_id64
        )


class AtmosphereComposition(Base):
    """Gasses held by gravity in a layer around a planet."""

    __tablename__ = "atmosphere_composition"

    name: Mapped[str] = mapped_column(primary_key=True)
    percentage: Mapped[float]

    body_id64: Mapped[int] = mapped_column(ForeignKey("body.id64"), primary_key=True)

    def __repr__(self):
        return (
            f"<AtmosphereComposition({self.percentage:.2%} "
            + f"{self.name}, body_id64={self.body_id64})>"
        )

    def __eq__(self, other: AtmosphereComposition) -> bool:
        return (
            self.name == other.name
            and self.percentage == other.percentage
            and self.body_id64 == other.body_id64
        )


class SolidComposition(Base):
    """Gross material classification of a planet's
    non-gaseous/non-liquid matter."""

    __tablename__ = "solid_composition"

    name: Mapped[str] = mapped_column(primary_key=True)
    percentage: Mapped[float]

    body_id64: Mapped[int] = mapped_column(ForeignKey("body.id64"), primary_key=True)

    def __repr__(self):
        return (
            f"<SolidComposition({self.percentage:.2%} "
            + f"{self.name}, body_id64={self.body_id64})>"
        )

    def __eq__(self, other: SolidComposition) -> bool:
        return (
            self.name == other.name
            and self.percentage == other.percentage
            and self.body_id64 == other.body_id64
        )


class Material(Base):
    """The relative abundance of a given raw material on a solid
    body."""

    __tablename__ = "material"

    name: Mapped[str] = mapped_column(primary_key=True)
    percentage: Mapped[float]

    body_id64: Mapped[int] = mapped_column(ForeignKey("body.id64"), primary_key=True)

    def __repr__(self):
        return (
            f"<Material({self.name!r}: {self.percentage:.6}, "
            + f"body_id64={self.body_id64 or 'pending'})>"
        )

    def __eq__(self, other: Material) -> bool:
        return (
            self.name == other.name
            and self.percentage == other.percentage
            and self.body_id64 == other.body_id64
        )


class DetectedSignal(Base):
    """How many of the named class of signals were detected on a
    body."""

    __tablename__ = "detected_signal"

    name: Mapped[str] = mapped_column(primary_key=True)
    quantity: Mapped[int]

    signals_id: Mapped[int] = mapped_column(ForeignKey("signals.id"), primary_key=True)

    def __repr__(self):
        return (
            f"<DetectedSignal({self.name!r}, "
            + f"quantity={self.quantity}, "
            + f"signals_id={self.signals_id or 'pending'})>"
        )

    def __eq__(self, other: DetectedSignal) -> bool:
        return (
            self.name == other.name
            and self.quantity == other.quantity
            and self.signals_id == other.signals_id
        )


class DetectedGenus(Base):
    """A genus of flora or fungi detected on a body."""

    __tablename__ = "detected_genus"

    name: Mapped[str] = mapped_column(primary_key=True)

    signals_id: Mapped[int] = mapped_column(ForeignKey("signals.id"), primary_key=True)

    def __repr__(self):
        return (
            f"<DetectedGenus({self.name!r}, "
            + f"signals_id={self.signals_id or 'pending'})>"
        )

    def __eq__(self, other: DetectedGenus) -> bool:
        return self.name == other.name and self.signals_id == other.signals_id


class Signals(Base):
    """What signals (and how many) were detected on a body or a ring."""

    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(primary_key=True)

    signals: Mapped[List["DetectedSignal"]] = relationship()
    genuses: Mapped[List["DetectedGenus"]] = relationship()
    updateTime: Mapped[datetime]

    body_id64: Mapped[int | None] = mapped_column(ForeignKey("body.id64"))
    ring_name: Mapped[str | None] = mapped_column(ForeignKey("ring.name"))

    def __repr__(self):
        return (
            f"<Signals({len(self.signals)} signals, "
            + f"{len(self.genuses)} genuses,"
            + f"body_id64={self.body_id64 or 'pending'})>"
        )

    def __eq__(self, other: Signals) -> bool:
        return (
            self.signals == other.signals
            and self.updateTime == other.updateTime
            and self.body_id64 == other.body_id64
        )


class Parent(Base):
    """Objects around which a body may orbit."""

    __tablename__ = "parent"

    name: Mapped[str] = mapped_column(primary_key=True)
    bodyId: Mapped[int] = mapped_column(primary_key=True)

    body_id64: Mapped[int] = mapped_column(ForeignKey("body.id64"), primary_key=True)

    def __repr__(self):
        return (
            f"<Parent({self.kind}: {self.bodyId}, "
            + f"body_id64={self.body_id64 or 'pending'})>"
        )

    def __eq__(self, other: Parent) -> bool:
        return (
            self.name == other.name
            and self.bodyId == other.bodyId
            and self.body_id64 == other.body_id64
        )


# rings: name/type/mass/innerRadius/outerRadius/signals
class Belt(Base):
    """Diffuse icy, metallic, or rocky debris in a relatively large
    orbit around one or more stars."""

    __tablename__ = "belt"

    name: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[str]
    mass: Mapped[int] = mapped_column(BigInteger)
    innerRadius: Mapped[int] = mapped_column(BigInteger)
    outerRadius: Mapped[int] = mapped_column(BigInteger)

    body_id64: Mapped[int] = mapped_column(ForeignKey("body.id64"))
    body: Mapped[Optional["Body"]] = relationship(back_populates="belts")

    def __repr__(self):
        return f"<Belt({self.name!r})>"

    def __eq__(self, other: Belt) -> bool:
        return (
            self.name == other.name
            and self.type == other.type
            and self.mass == other.mass
            and self.innerRadius == other.innerRadius
            and self.outerRadius == other.outerRadius
            and self.body_id64 == other.body_id64
        )


class Ring(Base):
    """Icy, metallic, or rocky debris in close orbit around a body and
    dense enough to be visible from tens to hundreds of lightseconds
    away."""

    __tablename__ = "ring"

    name: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[str]
    mass: Mapped[int] = mapped_column(BigInteger)
    innerRadius: Mapped[int] = mapped_column(BigInteger)
    outerRadius: Mapped[int] = mapped_column(BigInteger)
    signals: Mapped[Optional["Signals"]] = relationship()

    body_id64: Mapped[int] = mapped_column(ForeignKey("body.id64"))
    body: Mapped[Optional["Body"]] = relationship(back_populates="rings")

    def __repr__(self):
        return f"<Belt({self.name!r})>"

    def __eq__(self, other: Belt) -> bool:
        return (
            self.name == other.name
            and self.type == other.type
            and self.mass == other.mass
            and self.innerRadius == other.innerRadius
            and self.outerRadius == other.outerRadius
            and self.signals == other.signals
            and self.body_id64 == other.body_id64
        )


class BodyTimestamp(Base):
    """The dates and times of various body scans."""

    __tablename__ = "body_timestamp"

    name: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[datetime]

    body_id64: Mapped[int] = mapped_column(ForeignKey("body.id64"), primary_key=True)

    def __repr__(self):
        return (
            f"<BodyTimestamp({self.name!r} at "
            + f"value={self.value}, "
            + f"body_id64={self.body_id64 or 'pending'})>"
        )

    def __eq__(self, other: BodyTimestamp) -> bool:
        return (
            self.name == other.name
            and self.value == other.value
            and self.body_id64 == other.body_id64
        )


class Body(Base):
    """Astronomical objects within a system, including stars and planets."""

    __tablename__ = "body"

    id64: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    bodyId: Mapped[int]
    name: Mapped[str]
    type: Mapped[str]
    subType: Mapped[str | None]
    distanceToArrival: Mapped[float | None]
    mainStar: Mapped[bool | None]
    age: Mapped[int | None]
    spectralClass: Mapped[str | None]
    luminosity: Mapped[str | None]
    absoluteMagnitude: Mapped[float | None]
    solarMasses: Mapped[float | None]
    solarRadius: Mapped[float | None]
    isLandable: Mapped[bool | None]
    gravity: Mapped[float | None]
    earthMasses: Mapped[float | None]
    radius: Mapped[float | None]
    surfaceTemperature: Mapped[float | None]
    surfacePressure: Mapped[float | None]
    volcanismType: Mapped[str | None]
    atmosphereType: Mapped[str | None]
    atmosphereComposition: Mapped[List["AtmosphereComposition"]] = relationship()
    solidComposition: Mapped[List["SolidComposition"]] = relationship()
    terraformingState: Mapped[str | None]
    materials: Mapped[List["Material"]] = relationship()
    signals: Mapped[Optional["Signals"]] = relationship()
    reserveLevel: Mapped[str | None]
    rotationalPeriod: Mapped[float | None]
    rotationalPeriodTidallyLocked: Mapped[bool | None]
    axialTilt: Mapped[float | None]
    parents: Mapped[List["Parent"]] = relationship()
    orbitalPeriod: Mapped[float | None]
    semiMajorAxis: Mapped[float | None]
    orbitalEccentricity: Mapped[float | None]
    orbitalInclination: Mapped[float | None]
    argOfPeriapsis: Mapped[float | None]
    meanAnomaly: Mapped[float | None]
    ascendingNode: Mapped[float | None]
    belts: Mapped[List["Belt"]] = relationship(back_populates="body")
    rings: Mapped[List["Ring"]] = relationship(back_populates="body")
    timestamps: Mapped[List["BodyTimestamp"]] = relationship()
    stations: Mapped[List["Station"]] = relationship(back_populates="body")
    updateTime: Mapped[datetime]

    # a system may contain many bodies; model this as a
    # bi-directional, nullable, many-to-one relationship
    # (bodies:system)
    system_id64: Mapped[Optional[int]] = mapped_column(ForeignKey("system.id64"))
    system: Mapped[Optional["System"]] = relationship(back_populates="bodies")

    def __repr__(self):
        return f"<Body(id64={self.id64!r}, {self.name!r})>"

    def __eq__(self, other: Body) -> bool:
        return self.id64 == other.id64 and self.updateTime == other.updateTime


class StationEconomy(Base):
    """Stations can have multiple active market economies, which
    influences (or reflects) the station's services and commodity
    market.  This is modeled as a one-to-many relationship."""

    __tablename__ = "station_economy"

    name: Mapped[str] = mapped_column(primary_key=True)
    weight: Mapped[int]
    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"), primary_key=True)

    def __repr__(self):
        return (
            f"<StationEconomy({self.name!r}: {self.weight}, "
            + f"station_id={self.station_id or 'pending'})>"
        )

    def __eq__(self, other: StationEconomy) -> bool:
        return (
            self.name == other.name
            and self.weight == other.weight
            and self.station_id == other.station_id
        )


class StationService(Base):
    """What services a station provides, modeled as a one-to-many
    relationship."""

    __tablename__ = "station_service"

    name: Mapped[str] = mapped_column(primary_key=True)
    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"), primary_key=True)

    def __repr__(self):
        return f"<StationService({self.name!r}, station_id={self.station_id})>"

    def __eq__(self, other: StationService) -> bool:
        return self.name == other.name and self.station_id == other.station_id


class MarketOrder(Base):
    """What a station is buying or selling, modeled as a one-to-many
    relationship."""

    __tablename__ = "market_order"

    symbol: Mapped[str] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(primary_key=True)
    demand: Mapped[int]
    supply: Mapped[int]
    buyPrice: Mapped[int]
    sellPrice: Mapped[int]
    market_id: Mapped[int] = mapped_column(
        ForeignKey("market.station_id"), primary_key=True
    )

    def __repr__(self):
        return (
            f"<MarketOrder({'Buy' if self.demand else 'Sell'} "
            + f"{self.demand if self.demand else self.supply} "
            + f"{self.symbol} for "
            + f"{self.buyPrice if self.sellPrice else self.sellPrice} CR, "
            + f"market_id={self.market_id or 'pending'})>"
        )

    def __eq__(self, other: MarketOrder) -> bool:
        return (
            self.commodityId == other.symbol
            and self.category == other.category
            and self.demand == other.demand
            and self.supply == other.supply
            and self.buyPrice == other.buyPrice
            and self.sellPrice == other.sellPrice
            and self.market_id == other.market_id
        )


class ProhibitedCommodity(Base):
    """These commodities, listed by name in the Spansh galaxy data
    dump, are prohibited by the linked station."""

    __tablename__ = "prohibited_commodity"

    name: Mapped[str] = mapped_column(primary_key=True)
    market_id: Mapped[int] = mapped_column(
        ForeignKey("market.station_id"), primary_key=True
    )

    def __repr__(self):
        return f"<ProhibitedCommodity({self.name!r}, " + f"market_id={self.market_id})>"

    def __eq__(self, other: ProhibitedCommodity) -> bool:
        return self.name == other.name and self.market_id == other.market_id


class Market(Base):
    """A station's market, including market orders, prohibited
    commodities, and the last time the data was updated."""

    __tablename__ = "market"

    commodities: Mapped[List["MarketOrder"]] = relationship()
    prohibitedCommodities: Mapped[List["ProhibitedCommodity"]] = relationship()
    updateTime: Mapped[datetime]

    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"), primary_key=True)

    def __repr__(self):
        return f"<Market(station_id={self.station_id})>"

    def __eq__(self, other: Market) -> bool:
        return (
            self.station_id == other.station_id
            and self.updateTime == other.updateTime
            and self.commodities == other.commodities
            and self.prohibitedCommodities == other.prohibitedCommodities
        )


class ShipyardStock(Base):
    """Hulls for sale by a station's shipyard service."""

    __tablename__ = "shipyard_stock"

    name: Mapped[str]
    symbol: Mapped[str]
    shipId: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shipyard_id: Mapped[int] = mapped_column(
        ForeignKey("shipyard.station_id"), primary_key=True
    )

    def __repr__(self):
        return f"<Ship({self.name}, station_id={self.station_id})>"

    def __eq__(self, other: ShipyardStock) -> bool:
        return (
            self.name == other.name
            and self.symbol == other.symbol
            and self.shipId == other.shipId
            and self.shipyard_id == other.shipyard_id
        )


class Shipyard(Base):
    """A station's shipyard service."""

    __tablename__ = "shipyard"

    ships: Mapped[List["ShipyardStock"]] = relationship()
    updateTime: Mapped[datetime]

    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"), primary_key=True)

    def __repr__(self):
        return f"<Shipyard(station_id={self.station_id})>"

    def __eq__(self, other: Shipyard) -> bool:
        return (
            self.station_id == other.station_id
            and self.updateTime == other.updateTime
            and self.ships == other.ships
        )


class OutfittingStock(Base):
    """Modules for sale by a station's outfitting service."""

    __tablename__ = "outfitting_stock"

    # TODO: break name..ship out into separate class? but that would
    # require a SystemSchema-level de-duplication pass at
    # de-serialization time
    name: Mapped[str]
    symbol: Mapped[str]
    moduleId: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    class_: Mapped[int]
    rating: Mapped[str]
    category: Mapped[str]
    ship: Mapped[str | None]
    outfitting_id: Mapped[int] = mapped_column(
        ForeignKey("outfitting.station_id"), primary_key=True
    )

    def __repr__(self):
        return (
            f"<Module({self.rating}{self.class_} {self.name}, "
            + f"outfitting_id={self.outfitting_id or 'pending'})>"
        )

    def __eq__(self, other: OutfittingStock) -> bool:
        return (
            self.name == other.name
            and self.symbol == other.symbol
            and self.moduleId == other.moduleId
            and self.class_ == other.class_
            and self.rating == other.rating
            and self.category == other.category
            and self.ship == other.ship
            and self.station_id == other.station_id
        )


class Outfitting(Base):
    """A station's outfitting service."""

    __tablename__ = "outfitting"

    modules: Mapped[List["OutfittingStock"]] = relationship()
    updateTime: Mapped[datetime]

    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"), primary_key=True)

    def __repr__(self):
        return f"<Outfitting(station_id={self.station_id})>"

    def __eq__(self, other: Outfitting) -> bool:
        return (
            self.station_id == other.station_id
            and self.updateTime == other.updateTime
            and self.modules == other.modules
        )


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
    economies: Mapped[List["StationEconomy"]] = relationship()
    allegiance: Mapped[str | None]
    government: Mapped[str | None]
    services: Mapped[List["StationService"]] = relationship()
    type: Mapped[str | None]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    largeLandingPads: Mapped[int | None]  # landingPads
    mediumLandingPads: Mapped[int | None]
    smallLandingPads: Mapped[int | None]
    market: Mapped[Optional["Market"]] = relationship()
    shipyard: Mapped[Optional["Shipyard"]] = relationship()
    outfitting: Mapped[Optional["Outfitting"]] = relationship()

    # a system may contain many space stations; model this as a
    # bi-directional, nullable, many-to-one relationship
    # (stations:system)
    system_id64: Mapped[Optional[int]] = mapped_column(ForeignKey("system.id64"))
    system: Mapped[Optional["System"]] = relationship(back_populates="stations")

    # a body might support many surface ports; model this as a
    # bi-directional, nullable, many-to-one relationship
    # (stations:body)
    body_id64: Mapped[Optional[int]] = mapped_column(ForeignKey("body.id64"))
    body: Mapped[Optional["Body"]] = relationship(back_populates="stations")

    def __repr__(self):
        return (
            f"<Station({self.name!r}, "
            + f"system_id64={self.system_id64}, "
            + f"body_id64={self.body_id64})>"
        )

    def __eq__(self, other: Station) -> bool:
        return self.id == other.id and self.updateTime == self.updateTime


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
    factions: Mapped[List["FactionState"]] = relationship(back_populates="system")
    powers: Mapped[List["PowerPlay"]] = relationship()
    powerState: Mapped[str | None]
    date: Mapped[datetime]
    bodies: Mapped[List["Body"]] = relationship(back_populates="system")
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
        unknown = EXCLUDE
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_load
    def post_process_input(self, in_data, **kwargs):
        """Memoize this object using the Marshmallow context.  This
        removes duplicate Faction objects that violate the class's
        uniquness constraint.  (The ORM cannot detect this on its
        own.)"""
        # make sure we're being called after the Faction object was
        # created
        if not isinstance(in_data, Faction):
            return in_data

        # de-duplicate factions
        if in_data.name not in self.context["factions"]:
            self.context["factions"][in_data.name] = in_data
            return in_data
        else:
            return self.context["factions"][in_data.name]


class FactionStateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FactionState
        exclude = ["faction_name", "system_id64", "system"]
        include_fk = True
        include_relationships = True
        load_instance = True

    faction = Nested(FactionSchema)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        new_data = out_data.copy()

        # flatten the faction data
        faction = new_data.pop("faction")
        new_data.update(faction)

        return new_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""

        # wrap the faction data
        new_data = {
            "faction": in_data,
            "state": in_data["state"],
            "influence": in_data["influence"],
        }

        return new_data


class PowerPlaySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PowerPlay
        exclude = ["system_id64"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return out_data.get("power")

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        return {"power": in_data}


class StationEconomySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StationEconomy
        exclude = ["station_id"]
        include_fk = True
        include_relationships = True
        load_instance = True


class StationServiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StationService
        exclude = ["station_id"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return out_data.get("name")

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        return {"name": in_data}


class MarketOrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MarketOrder
        exclude = ["market_id"]
        unknown = EXCLUDE
        include_fk = True
        include_relationships = True
        load_instance = True


class ProhibitedCommoditySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProhibitedCommodity
        exclude = ["market_id"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return out_data.get("name")

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        # TODO: translate to the commodity's symbolic name
        return {"name": in_data}


class MarketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Market
        exclude = ["station_id"]
        include_fk = True
        include_relationships = True
        load_instance = True

    commodities = Nested(MarketOrderSchema, many=True, required=False)
    prohibitedCommodities = Nested(ProhibitedCommoditySchema, many=True, required=False)


class ShipyardStockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ShipyardStock
        exclude = ["shipyard_id"]
        include_fk = True
        include_relationships = True
        load_instance = True


class ShipyardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Shipyard
        exclude = ["station_id"]
        include_fk = True
        include_relationships = True
        load_instance = True

    ships = Nested(ShipyardStockSchema, many=True, required=False)


class OutfittingStockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OutfittingStock
        exclude = ["outfitting_id"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        out_data["class"] = out_data.pop("class_")
        return out_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        new_data = in_data.copy()
        new_data["class_"] = new_data.pop("class")
        return new_data


class OutfittingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Outfitting
        exclude = ["station_id"]
        include_fk = True
        include_relationships = True
        load_instance = True

    modules = Nested(OutfittingStockSchema, many=True, required=False)


class StationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Station
        exclude = ["controllingFaction_id", "system_id64", "system"]
        include_fk = True
        include_relationships = True
        load_instance = True

    controllingFaction = Nested(FactionSchema, required=False, allow_none=True)
    economies = Nested(StationEconomySchema, many=True, required=False)
    services = Nested(StationServiceSchema, many=True, required=False)
    market = Nested(MarketSchema, required=False)
    shipyard = Nested(ShipyardSchema, required=False)
    outfitting = Nested(OutfittingSchema, required=False)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""

        # convert 0.0 to 0
        float_columns = [
            "distanceToArrival",
        ]
        for k in float_columns:
            if k in out_data and out_data[k] == 0.0:
                out_data[k] = 0

        # remove empty keys to save space
        required_columns = ["name", "id", "updateTime"]
        for k in set(out_data.keys()) - set(required_columns):
            if out_data.get(k) is None or out_data.get(k) == []:
                out_data.pop(k)

        # flatten controllingFaction
        if "controllingFaction" in out_data:
            controlling_faction = out_data.get("controllingFaction", {})
            out_data["controllingFaction"] = controlling_faction.get("name")
            if "controllingFactionState" not in out_data:
                # FIXME: why does Spansh do this?
                out_data["controllingFactionState"] = None

        # rewrap economies
        if "economies" in out_data:
            out_data["economies"] = {
                economy.get("name"): economy.get("weight")
                for economy in out_data["economies"]
            }

        # wrap landingPads
        landingPads = {}
        for k_new, k_orig in [
            ("large", "largeLandingPads"),
            ("medium", "mediumLandingPads"),
            ("small", "smallLandingPads"),
        ]:
            if k_orig in out_data:
                landingPads[k_new] = out_data.pop(k_orig)
        if landingPads:
            out_data["landingPads"] = landingPads

        return out_data

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

        # rewrap economies
        if "economies" in new_data:
            new_data["economies"] = [
                {"name": economy, "weight": weight}
                for economy, weight in new_data["economies"].items()
            ]

        # flatten landingPads
        landingPads = new_data.pop("landingPads", {})
        if landingPads:
            new_data["largeLandingPads"] = landingPads.get("large")
            new_data["mediumLandingPads"] = landingPads.get("medium")
            new_data["smallLandingPads"] = landingPads.get("small")

        return new_data


class AtmosphereCompositionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AtmosphereComposition
        exclude = ["body_id64"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return {out_data["name"]: out_data["percentage"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        return {"name": in_data[0], "percentage": in_data[1]}


class SolidCompositionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SolidComposition
        exclude = ["body_id64"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return {out_data["name"]: out_data["percentage"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        return {"name": in_data[0], "percentage": in_data[1]}


class MaterialSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Material
        exclude = ["body_id64"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return {out_data["name"]: out_data["percentage"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {"name": in_data[0], "percentage": in_data[1]}


class DetectedSignalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DetectedSignal
        exclude = ["signals_id"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return {out_data["name"]: out_data["quantity"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return {"name": in_data[0], "quantity": in_data[1]}


class DetectedGenusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DetectedGenus
        exclude = ["signals_id"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return out_data["name"]

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return {"name": in_data}


class SignalsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Signals
        exclude = ["id", "body_id64", "ring_name"]
        include_fk = True
        include_relationships = True
        load_instance = True

    signals = Nested(DetectedSignalSchema, many=True, required=False)
    genuses = Nested(DetectedGenusSchema, many=True, required=False)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""

        # rewrap signals
        out_data["signals"] = dict(ChainMap(*out_data["signals"]))

        return out_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        in_data = in_data.copy()

        # rewrap signals
        in_data["signals"] = list(in_data["signals"].items())

        return in_data


class ParentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Parent
        exclude = ["body_id64"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return {out_data["name"]: out_data["bodyId"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        [(name, bodyId)] = in_data.items()
        return {"name": name, "bodyId": bodyId}


class BeltSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Belt
        exclude = ["body_id64", "body"]
        include_fk = True
        include_relationships = True
        load_instance = True


class RingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ring
        exclude = ["body_id64", "body"]
        include_fk = True
        include_relationships = True
        load_instance = True

    signals = Nested(SignalsSchema, required=False)


class BodyTimestampSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BodyTimestamp
        exclude = ["body_id64"]
        include_fk = True
        include_relationships = True
        load_instance = True

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""
        return {out_data["name"]: out_data["value"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        return {"name": in_data[0], "value": in_data[1]}


class BodySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Body
        include_fk = True
        include_relationships = True
        load_instance = True

    atmosphereComposition = Nested(
        AtmosphereCompositionSchema, many=True, required=False
    )
    solidComposition = Nested(SolidCompositionSchema, many=True, required=False)
    materials = Nested(MaterialSchema, many=True, required=False)
    signals = Nested(SignalsSchema, required=False)
    parents = Nested(ParentSchema, many=True, required=False)
    belts = Nested(BeltSchema, many=True, required=False)
    rings = Nested(RingSchema, many=True, required=False)
    timestamps = Nested(BodyTimestampSchema, many=True, required=False)
    stations = Nested(StationSchema, many=True, required=False)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""

        # remove empty keys to save space
        required_columns = ["id64", "bodyId", "name", "type", "updateTime"]
        for k in set(out_data.keys()) - set(required_columns):
            if out_data.get(k) is None or out_data.get(k) == []:
                out_data.pop(k)

        # rewrap atmosphereComposition
        if "atmosphereComposition" in out_data:
            out_data["atmosphereComposition"] = dict(
                ChainMap(*out_data["atmosphereComposition"])
            )

        # rewrap solidComposition
        if "solidComposition" in out_data:
            out_data["solidComposition"] = dict(ChainMap(*out_data["solidComposition"]))

        # rewrap materials
        if "materials" in out_data:
            out_data["materials"] = dict(ChainMap(*out_data["materials"]))

        # rewrap timestamps
        if "timestamps" in out_data:
            out_data["timestamps"] = dict(ChainMap(*out_data["timestamps"]))

        return out_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        in_data = in_data.copy()

        # rewrap atmosphereComposition
        if "atmosphereComposition" in in_data:
            in_data["atmosphereComposition"] = list(
                in_data["atmosphereComposition"].items()
            )

        # rewrap solidComposition
        if "solidComposition" in in_data:
            in_data["solidComposition"] = list(in_data["solidComposition"].items())

        # rewrap materials
        if "materials" in in_data:
            in_data["materials"] = list(in_data["materials"].items())

        # rewrap timestamps
        if "timestamps" in in_data:
            in_data["timestamps"] = list(in_data["timestamps"].items())

        return in_data


class SystemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = System
        exclude = ["controllingFaction_id"]
        include_fk = True
        include_relationships = True
        load_instance = True
        ordered = True  # see note below

    # NOTE: Order is significant!  Process factions first!  Sometimes,
    # a station's faction data is wrong.
    factions = Nested(FactionStateSchema, many=True, required=False)

    controllingFaction = Nested(FactionSchema, required=False, allow_none=True)
    powers = Nested(PowerPlaySchema, many=True, required=False)
    bodies = Nested(BodySchema, many=True, required=False)
    stations = Nested(StationSchema, many=True, required=False)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        """Mimick the Spansh galaxy data dump format as best we can."""

        # wrap coords
        coords = {
            "x": out_data.pop("x"),
            "y": out_data.pop("y"),
            "z": out_data.pop("z"),
        }
        out_data["coords"] = coords

        # remove empty keys to save space
        required_columns = ["id64", "name", "coords", "date", "bodies", "stations"]
        for k in set(out_data.keys()) - set(required_columns):
            if out_data.get(k) is None or out_data.get(k) == []:
                out_data.pop(k)

        return out_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        new_data = in_data.copy()

        # flatten coords
        coords = new_data.pop("coords")
        new_data.update(coords)

        return new_data

    @pre_load
    def init_context(self, in_data, **kwargs):
        """Initialize the de-serialization context if the caller
        didn't."""
        if not self.context:
            self.context["factions"] = {}
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
