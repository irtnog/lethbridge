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

import logging
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)

# configure module-level logging
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """This class tracks ORM class definitions and related metadata
    for the tables created in this module."""

    # FIXME: implement this constraint using a BEFORE UPDATE trigger
    # instead of the @validates decorator?
    def value_must_increase(self, key, new_value):
        old_value = getattr(self, key, None)
        if old_value and old_value >= new_value:
            raise ValueError(
                f"Update uses outdated data for {self!r}: "
                + f"old_value={old_value!r}, new_value={new_value!r}"
            )
        return new_value


class FactionState(Base):
    """A faction's influence over and status within a given system.

    This models a faction's state in the background simulation as a
    bi-directional association table in the SQLAlchemy ORM since this
    state includes data beyond the system/faction many-to-many
    relationship."""

    __tablename__ = "faction_state"

    # TODO: happiness? not in Spansh dumps
    influence: Mapped[Decimal]
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


class ThargoidWar(Base):
    """The state of the Second Thargoid War in an affected system,
    modeled as a one-to-one relationship."""

    __tablename__ = "thargoid_war"

    currentState: Mapped[str | None]
    successState: Mapped[str | None]
    failureState: Mapped[str | None]
    progress: Mapped[Decimal | None]
    daysRemaining: Mapped[int | None]
    portsRemaining: Mapped[int | None]
    successReached: Mapped[bool | None]

    system_id64: Mapped[int] = mapped_column(
        ForeignKey("system.id64"),
        primary_key=True,
    )

    def __repr__(self):
        return (
            f"<ThargoidWar(system_id64={self.system_id64 or 'pending'}, "
            + f"{self.currentState})>"
        )

    def __eq__(self, other: ThargoidWar) -> bool:
        return (
            self.currentState == other.currentState
            and self.successState == other.successState
            and self.failureState == other.failureState
            and self.progress == other.progress
            and self.daysRemaining == other.daysRemaining
            and self.portsRemaining == other.portsRemaining
            and self.successReached == other.successReached
            and self.system_id64 == other.system_id64
        )


class AtmosphereComposition(Base):
    """Gasses held by gravity in a layer around a planet."""

    __tablename__ = "atmosphere_composition"

    name: Mapped[str] = mapped_column(primary_key=True)
    percentage: Mapped[Decimal]

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
    percentage: Mapped[Decimal]

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
    percentage: Mapped[Decimal]

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

    @validates("updateTime")
    def value_must_increase(self, key, new_value):
        return super().value_must_increase(key, new_value)


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

    @validates("value")
    def value_must_increase(self, key, new_value):
        return super().value_must_increase(key, new_value)


class Body(Base):
    """Astronomical objects within a system, including stars and planets."""

    __tablename__ = "body"

    id64: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    bodyId: Mapped[int]
    name: Mapped[str]
    type: Mapped[str]
    subType: Mapped[str | None]
    distanceToArrival: Mapped[Decimal | None]
    mainStar: Mapped[bool | None]
    age: Mapped[int | None]
    spectralClass: Mapped[str | None]
    luminosity: Mapped[str | None]
    absoluteMagnitude: Mapped[Decimal | None]
    solarMasses: Mapped[Decimal | None]
    solarRadius: Mapped[Decimal | None]
    isLandable: Mapped[bool | None]
    gravity: Mapped[Decimal | None]
    earthMasses: Mapped[Decimal | None]
    radius: Mapped[Decimal | None]
    surfaceTemperature: Mapped[Decimal | None]
    surfacePressure: Mapped[Decimal | None]
    volcanismType: Mapped[str | None]
    atmosphereType: Mapped[str | None]
    atmosphereComposition: Mapped[List["AtmosphereComposition"]] = relationship()
    solidComposition: Mapped[List["SolidComposition"]] = relationship()
    terraformingState: Mapped[str | None]
    materials: Mapped[List["Material"]] = relationship()
    signals: Mapped[Optional["Signals"]] = relationship()
    reserveLevel: Mapped[str | None]
    rotationalPeriod: Mapped[Decimal | None]
    rotationalPeriodTidallyLocked: Mapped[bool | None]
    axialTilt: Mapped[Decimal | None]
    parents: Mapped[List["Parent"]] = relationship()
    orbitalPeriod: Mapped[Decimal | None]
    semiMajorAxis: Mapped[Decimal | None]
    orbitalEccentricity: Mapped[Decimal | None]
    orbitalInclination: Mapped[Decimal | None]
    argOfPeriapsis: Mapped[Decimal | None]
    meanAnomaly: Mapped[Decimal | None]
    ascendingNode: Mapped[Decimal | None]
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

    @validates("updateTime")
    def value_must_increase(self, key, new_value):
        return super().value_must_increase(key, new_value)


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

    # name
    symbol: Mapped[str] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(primary_key=True)
    # commodityId
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
            self.symbol == other.symbol
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

    @validates("updateTime")
    def value_must_increase(self, key, new_value):
        return super().value_must_increase(key, new_value)


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

    @validates("updateTime")
    def value_must_increase(self, key, new_value):
        return super().value_must_increase(key, new_value)


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

    @validates("updateTime")
    def value_must_increase(self, key, new_value):
        return super().value_must_increase(key, new_value)


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
    distanceToArrival: Mapped[Decimal | None]
    primaryEconomy: Mapped[str | None]
    economies: Mapped[List["StationEconomy"]] = relationship()
    allegiance: Mapped[str | None]
    government: Mapped[str | None]
    services: Mapped[List["StationService"]] = relationship()
    type: Mapped[str | None]
    latitude: Mapped[Decimal | None]
    longitude: Mapped[Decimal | None]
    largeLandingPads: Mapped[int | None]  # landingPads
    mediumLandingPads: Mapped[int | None]
    smallLandingPads: Mapped[int | None]
    market: Mapped[Optional["Market"]] = relationship()
    shipyard: Mapped[Optional["Shipyard"]] = relationship()
    outfitting: Mapped[Optional["Outfitting"]] = relationship()

    # a body might support many surface ports; model this as a
    # bi-directional, nullable, many-to-one relationship
    # (stations:body)
    body_id64: Mapped[Optional[int]] = mapped_column(ForeignKey("body.id64"))
    body: Mapped[Optional["Body"]] = relationship(back_populates="stations")

    # a system may contain many space stations; model this as a
    # bi-directional, nullable, many-to-one relationship
    # (stations:system)
    system_id64: Mapped[Optional[int]] = mapped_column(ForeignKey("system.id64"))
    system: Mapped[Optional["System"]] = relationship(back_populates="stations")

    def __repr__(self):
        return (
            f"<Station({self.name!r}, "
            + f"system_id64={self.system_id64}, "
            + f"body_id64={self.body_id64})>"
        )

    def __eq__(self, other: Station) -> bool:
        return self.id == other.id and self.updateTime == self.updateTime

    @validates("updateTime")
    def value_must_increase(self, key, new_value):
        return super().value_must_increase(key, new_value)


class System(Base):
    """A gravitationally bound group of stars, planets, and other
    bodies."""

    __tablename__ = "system"

    id64: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]  # not unique, e.g., AH Cancri
    x: Mapped[Decimal]  # coords
    y: Mapped[Decimal]
    z: Mapped[Decimal]
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
    thargoidWar: Mapped[Optional["ThargoidWar"]] = relationship()
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
            and self.bodies == other.bodies
            and self.stations == other.stations
        )

    @validates("date")
    def value_must_increase(self, key, new_value):
        return super().value_must_increase(key, new_value)
