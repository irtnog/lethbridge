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
    relationship."""

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
    relationship."""

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


class Body(Base):
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
    atmosphereType: Mapped[str | None]
    # atmosphereComposition: Mapped[List["AtmosphereComposition"]]...
    # solidComposition: Mapped[List["SolidComposition"]]...
    terraformingState: Mapped[str | None]
    rotationalPeriod: Mapped[float | None]
    rotationalPeriodTidallyLocked: Mapped[bool | None]
    axialTilt: Mapped[float | None]
    # parents
    orbitalPeriod: Mapped[float | None]
    semiMajorAxis: Mapped[float | None]
    orbitalEccentricity: Mapped[float | None]
    orbitalInclination: Mapped[float | None]
    argOfPeriapsis: Mapped[float | None]
    meanAnomaly: Mapped[float | None]
    ascendingNode: Mapped[float | None]
    # timestamps: Mapped[List["BodyTimestamp"]]...
    stations: Mapped[List["Station"]] = relationship(back_populates="body")
    updateTime: Mapped[datetime]

    # a system may contain many bodies; model this as a
    # bi-directional, nullable, many-to-one relationship
    # (bodies:system)
    system_id64: Mapped[Optional[int]] = mapped_column(ForeignKey("system.id64"))
    system: Mapped[Optional["System"]] = relationship(back_populates="bodies")


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
            + f"station_id={self.station_id})>"
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

    # TODO: break name..commodityId out into separate class? but that
    # would require a SystemSchema-level de-duplication pass at
    # de-serialization time
    name: Mapped[str]
    symbol: Mapped[str]
    category: Mapped[str]
    commodityId: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    demand: Mapped[int]
    supply: Mapped[int]
    buyPrice: Mapped[int]
    sellPrice: Mapped[int]
    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"), primary_key=True)

    def __repr__(self):
        return (
            f"<MarketOrder({'Buy' if self.demand else 'Sell'} "
            + f"{self.demand if self.demand else self.supply} "
            + f"{self.name} for "
            + f"{self.buyPrice if self.sellPrice else self.sellPrice} CR, "
            + f"station_id={self.station_id})>"
        )

    def __eq__(self, other: MarketOrder) -> bool:
        return (
            self.commodityId == other.commodityId
            and self.demand == other.demand
            and self.supply == other.supply
            and self.buyPrice == other.buyPrice
            and self.sellPrice == other.sellPrice
            and self.station_id == other.station_id
        )


class ProhibitedCommodity(Base):
    """These commodities, listed by name in the Spansh galaxy data
    dump, are prohibited by the linked station."""

    __tablename__ = "prohibited_commodity"

    # TODO: link somehow to a future Commodity class? don't forget to
    # modify the serialization schema if you do
    name: Mapped[str] = mapped_column(primary_key=True)
    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"), primary_key=True)

    def __repr__(self):
        return (
            f"<ProhibitedCommodity({self.name!r}, " + f"station_id={self.station_id})>"
        )

    def __eq__(self, other: ProhibitedCommodity) -> bool:
        return self.name == other.name and self.station_id == other.station_id


class ShipyardStock(Base):
    """Hulls for sale by a station's shipyard service."""

    __tablename__ = "shipyard_stock"

    # TODO: break name..shipId out into separate class? but that would
    # require a SystemSchema-level de-duplication pass at
    # de-serialization time
    name: Mapped[str]
    symbol: Mapped[str]
    shipId: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"), primary_key=True)

    def __repr__(self):
        return f"<Ship({self.name}, station_id={self.station_id})>"

    def __eq__(self, other: ShipyardStock) -> bool:
        return (
            self.name == other.name
            and self.symbol == other.symbol
            and self.shipId == other.shipId
            and self.station_id == other.station_id
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
    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"), primary_key=True)

    def __repr__(self):
        return (
            f"<Module({self.rating}{self.class_} {self.name}, "
            + f"station_id={self.station_id})>"
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
    allegiance: Mapped[str | None]  # matches controllingFaction?
    government: Mapped[str | None]  # matches controllingFaction?
    services: Mapped[List["StationService"]] = relationship()
    type: Mapped[str | None]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    largeLandingPads: Mapped[int | None]  # landingPads
    mediumLandingPads: Mapped[int | None]
    smallLandingPads: Mapped[int | None]
    marketOrders: Mapped[List["MarketOrder"]] = relationship()  # market
    prohibitedCommodities: Mapped[List["ProhibitedCommodity"]] = relationship()
    marketUpdateTime: Mapped[datetime | None]
    shipyardShips: Mapped[List["ShipyardStock"]] = relationship()
    shipyardUpdateTime: Mapped[datetime | None]
    outfittingModules: Mapped[List["OutfittingStock"]] = relationship()
    outfittingUpdateTime: Mapped[datetime | None]

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

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        """Given incoming data that follows the Spansh galaxy data
        dump format, convert it into the representation expected by
        this schema."""
        return {
            "faction": in_data,
            "state": in_data["state"],
            "influence": in_data["influence"],
        }


class PowerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Power
        exclude = ["systems"]
        unknown = EXCLUDE
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
        exclude = ["station_id"]
        include_fk = True
        include_relationships = True
        load_instance = True


class ProhibitedCommoditySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProhibitedCommodity
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


class ShipyardStockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ShipyardStock
        exclude = ["station_id"]
        include_fk = True
        include_relationships = True
        load_instance = True


class OutfittingStockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OutfittingStock
        exclude = ["station_id"]
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


class StationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Station
        exclude = ["controllingFaction_id", "system_id64", "system"]
        unknown = EXCLUDE  # FIXME
        include_fk = True
        include_relationships = True
        load_instance = True

    controllingFaction = Nested(FactionSchema, required=False, allow_none=True)
    economies = Nested(StationEconomySchema, many=True, required=False)
    services = Nested(StationServiceSchema, many=True, required=False)
    marketOrders = Nested(MarketOrderSchema, many=True, required=False)
    prohibitedCommodities = Nested(ProhibitedCommoditySchema, many=True, required=False)
    shipyardShips = Nested(ShipyardStockSchema, many=True, required=False)
    outfittingModules = Nested(OutfittingStockSchema, many=True, required=False)

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

        # wrap market
        if "marketUpdateTime" in out_data:
            out_data["market"] = {
                # FIXME: Can a market that doesn't buy or sell
                # anything have a list of prohibited commodities?
                "commodities": out_data.pop("marketOrders", []),
                # The reverse is definitely true, e.g., fleet carrier
                # markets like WZL-B9Z in S171 43 in the sample data.
                "prohibitedCommodities": out_data.pop("prohibitedCommodities", []),
                # FIXME: assumes markets always have updateTime
                # attributes
                "updateTime": out_data.pop("marketUpdateTime"),
            }

        # wrap shipyard
        if "shipyardUpdateTime" in out_data:
            out_data["shipyard"] = {
                "ships": out_data.pop("shipyardShips"),
                "updateTime": out_data.pop("shipyardUpdateTime"),
            }

        # wrap outfitting
        if "outfittingUpdateTime" in out_data:
            out_data["outfitting"] = {
                "modules": out_data.pop("outfittingModules"),
                "updateTime": out_data.pop("outfittingUpdateTime"),
            }

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

        # flatten market
        if "market" in new_data:
            new_data["marketOrders"] = new_data.get("market").get("commodities")
            new_data["prohibitedCommodities"] = new_data.get("market").get(
                "prohibitedCommodities"
            )
            new_data["marketUpdateTime"] = new_data.get("market").get("updateTime")
            new_data.pop("market")

        # flatten shipyard
        if "shipyard" in new_data:
            new_data["shipyardShips"] = new_data.get("shipyard").get("ships")
            new_data["shipyardUpdateTime"] = new_data.get("shipyard").get("updateTime")

        # flatten outfitting
        if "outfitting" in new_data:
            new_data["outfittingModules"] = new_data.get("outfitting").get("modules")
            new_data["outfittingUpdateTime"] = new_data.get("outfitting").get(
                "updateTime"
            )
            new_data.pop("outfitting")

        return new_data


class BodySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Body
        unknown = EXCLUDE  # FIXME
        include_fk = True
        include_relationships = True
        load_instance = True

    stations = Nested(StationSchema, many=True, required=False)


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
    factions = Nested(StateSchema, many=True, required=False)

    controllingFaction = Nested(FactionSchema, required=False, allow_none=True)
    powers = Nested(PowerPlaySchema, many=True, required=False)
    bodies = Nested(BodySchema, many=True, required=False)
    stations = Nested(StationSchema, many=True, required=False)

    # TODO: translate between 'Anarchy'/'None' and None
    # TODO: powerState key denotes Bubble system?

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
