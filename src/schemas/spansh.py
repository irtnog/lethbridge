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

import logging
from collections import ChainMap

import simplejson
from marshmallow import EXCLUDE, post_dump, post_load, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemyAutoSchemaOpts
from marshmallow_sqlalchemy.fields import Nested

from ..database import (
    AtmosphereComposition,
    Belt,
    Body,
    BodyTimestamp,
    DetectedGenus,
    DetectedSignal,
    Faction,
    FactionState,
    Market,
    MarketOrder,
    Material,
    Outfitting,
    OutfittingStock,
    Parent,
    PowerPlay,
    ProhibitedCommodity,
    Ring,
    Shipyard,
    ShipyardStock,
    Signals,
    SolidComposition,
    Station,
    StationEconomy,
    StationService,
    System,
    ThargoidWar,
)

# configure module-level logging
logger = logging.getLogger(__name__)


# use the same configuration for all schemas
class BaseOpts(SQLAlchemyAutoSchemaOpts):
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, "render_module"):
            meta.render_module = simplejson
        if not hasattr(meta, "load_instance"):
            meta.load_instance = True
        super(BaseOpts, self).__init__(meta, ordered=ordered)


class BaseSchema(SQLAlchemyAutoSchema):
    OPTIONS_CLASS = BaseOpts


class FactionSchema(BaseSchema):
    class Meta:
        model = Faction
        unknown = EXCLUDE

    @post_load
    def post_process_input(self, in_data, **kwargs):
        """Memoize this object using the Marshmallow context (if so
        configured).  This removes duplicate Faction objects that
        violate the class's uniquness constraint, which ORM cannot
        detect on its own."""
        if not isinstance(in_data, Faction) or "factions" not in self.context:
            return in_data
        if in_data.name not in self.context["factions"]:
            self.context["factions"][in_data.name] = in_data
            return in_data
        else:
            return self.context["factions"][in_data.name]


class FactionStateSchema(BaseSchema):
    class Meta:
        model = FactionState

    faction = Nested(FactionSchema)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        out_data = out_data.copy()
        faction = out_data.pop("faction")
        out_data.update(faction)
        return out_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {
            "faction": in_data,
            "state": in_data["state"],
            "influence": in_data["influence"],
        }


class PowerPlaySchema(BaseSchema):
    class Meta:
        model = PowerPlay

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return out_data.get("power")

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {"power": in_data}


class ThargoidWarSchema(BaseSchema):
    class Meta:
        model = ThargoidWar


class StationEconomySchema(BaseSchema):
    class Meta:
        model = StationEconomy

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return {out_data["name"]: out_data["weight"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {"name": in_data[0], "weight": in_data[1]}


class StationServiceSchema(BaseSchema):
    class Meta:
        model = StationService

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return out_data.get("name")

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {"name": in_data}


class MarketOrderSchema(BaseSchema):
    class Meta:
        model = MarketOrder
        unknown = EXCLUDE


class ProhibitedCommoditySchema(BaseSchema):
    class Meta:
        model = ProhibitedCommodity

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return out_data.get("name")

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        # TODO: translate to the commodity's symbolic name
        return {"name": in_data}


class MarketSchema(BaseSchema):
    class Meta:
        model = Market

    commodities = Nested(MarketOrderSchema, many=True, required=False)
    prohibitedCommodities = Nested(ProhibitedCommoditySchema, many=True, required=False)


class ShipyardStockSchema(BaseSchema):
    class Meta:
        model = ShipyardStock


class ShipyardSchema(BaseSchema):
    class Meta:
        model = Shipyard

    ships = Nested(ShipyardStockSchema, many=True, required=False)


class OutfittingStockSchema(BaseSchema):
    class Meta:
        model = OutfittingStock

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        out_data["class"] = out_data.pop("class_")
        if not out_data.get("ship"):
            out_data.pop("ship")
        return out_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        in_data = in_data.copy()
        in_data["class_"] = in_data.pop("class")
        return in_data


class OutfittingSchema(BaseSchema):
    class Meta:
        model = Outfitting

    modules = Nested(OutfittingStockSchema, many=True, required=False)


class StationSchema(BaseSchema):
    class Meta:
        model = Station

    controllingFaction = Nested(FactionSchema, required=False, allow_none=True)
    economies = Nested(StationEconomySchema, many=True, required=False)
    services = Nested(StationServiceSchema, many=True, required=False)
    market = Nested(MarketSchema, required=False)
    shipyard = Nested(ShipyardSchema, required=False)
    outfitting = Nested(OutfittingSchema, required=False)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
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
            out_data["economies"] = dict(ChainMap(*out_data["economies"]))

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
        in_data = in_data.copy()

        # wrap faction data but preserve station-level allegiance and
        # government
        if "controllingFaction" in in_data:
            in_data["controllingFaction"] = {
                "name": in_data.get("controllingFaction"),
                "allegiance": in_data.get("allegiance"),
                "government": in_data.get("government"),
            }

        # rewrap economies
        if "economies" in in_data:
            in_data["economies"] = list(in_data["economies"].items())

        # flatten landingPads
        landingPads = in_data.pop("landingPads", {})
        if landingPads:
            in_data["largeLandingPads"] = landingPads.get("large")
            in_data["mediumLandingPads"] = landingPads.get("medium")
            in_data["smallLandingPads"] = landingPads.get("small")

        return in_data


class AtmosphereCompositionSchema(BaseSchema):
    class Meta:
        model = AtmosphereComposition

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return {out_data["name"]: out_data["percentage"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {"name": in_data[0], "percentage": in_data[1]}


class SolidCompositionSchema(BaseSchema):
    class Meta:
        model = SolidComposition

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return {out_data["name"]: out_data["percentage"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {"name": in_data[0], "percentage": in_data[1]}


class MaterialSchema(BaseSchema):
    class Meta:
        model = Material

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return {out_data["name"]: out_data["percentage"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {"name": in_data[0], "percentage": in_data[1]}


class DetectedSignalSchema(BaseSchema):
    class Meta:
        model = DetectedSignal

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return {out_data["name"]: out_data["quantity"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {"name": in_data[0], "quantity": in_data[1]}


class DetectedGenusSchema(BaseSchema):
    class Meta:
        model = DetectedGenus

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return out_data["name"]

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {"name": in_data}


class SignalsSchema(BaseSchema):
    class Meta:
        model = Signals
        exclude = ["id"]

    signals = Nested(DetectedSignalSchema, many=True, required=False)
    genuses = Nested(DetectedGenusSchema, many=True, required=False)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        if not out_data["genuses"]:
            # FIXME: should this output an empty list of genuses?
            # cf. 36 Ophiuchi C 9 a and C 10 a in the test data
            out_data.pop("genuses")
        out_data["signals"] = dict(ChainMap(*out_data["signals"]))
        return out_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        in_data = in_data.copy()
        in_data["signals"] = list(in_data["signals"].items())
        return in_data


class ParentSchema(BaseSchema):
    class Meta:
        model = Parent

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return {out_data["name"]: out_data["bodyId"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        [(name, bodyId)] = in_data.items()
        return {"name": name, "bodyId": bodyId}


class BeltSchema(BaseSchema):
    class Meta:
        model = Belt


class RingSchema(BaseSchema):
    class Meta:
        model = Ring

    signals = Nested(SignalsSchema, required=False)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        if not out_data["signals"]:
            out_data.pop("signals")
        return out_data


class BodyTimestampSchema(BaseSchema):
    class Meta:
        model = BodyTimestamp

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        return {out_data["name"]: out_data["value"]}

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        return {"name": in_data[0], "value": in_data[1]}


class BodySchema(BaseSchema):
    class Meta:
        model = Body

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
        # remove empty keys to save space
        required_columns = ["id64", "bodyId", "name", "type", "stations", "updateTime"]
        for k in set(out_data.keys()) - set(required_columns):
            if out_data.get(k) is None or out_data.get(k) == []:
                out_data.pop(k)

        # convert lists of key/value pairs into dictionaries
        for attribute in [
            "atmosphereComposition",
            "solidComposition",
            "materials",
            "timestamps",
        ]:
            if attribute in out_data:
                out_data[attribute] = dict(ChainMap(*out_data[attribute]))

        return out_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        # convert dictionaries into lists of key-value pairs
        in_data = in_data.copy()  # FIXME: avoid if unnecessary?
        for attribute in [
            "atmosphereComposition",
            "solidComposition",
            "materials",
            "timestamps",
        ]:
            if attribute in in_data:
                in_data[attribute] = list(in_data[attribute].items())
        return in_data


class SystemSchema(BaseSchema):
    class Meta:
        model = System
        ordered = True

    # NOTE: Order is significant!  Process the factions list first
    # because sometimes a station's faction data is wrong.
    factions = Nested(FactionStateSchema, many=True, required=False)
    controllingFaction = Nested(FactionSchema, required=False, allow_none=True)
    powers = Nested(PowerPlaySchema, many=True, required=False)
    thargoidWar = Nested(ThargoidWarSchema, required=False)
    bodies = Nested(BodySchema, many=True, required=False)
    stations = Nested(StationSchema, many=True, required=False)

    @post_dump
    def post_process_output(self, out_data, **kwargs):
        # wrap coords
        out_data["coords"] = {
            "x": out_data.pop("x"),
            "y": out_data.pop("y"),
            "z": out_data.pop("z"),
        }

        # remove empty keys to save space
        required_columns = ["id64", "name", "coords", "date", "bodies", "stations"]
        for k in set(out_data.keys()) - set(required_columns):
            if out_data.get(k) is None or out_data.get(k) == []:
                out_data.pop(k)

        return out_data

    @pre_load
    def pre_process_input(self, in_data, **kwargs):
        # flatten coords
        in_data = in_data.copy()
        coords = in_data.pop("coords")
        in_data.update(coords)
        return in_data

    @pre_load
    def init_context(self, in_data, **kwargs):
        """Initialize the de-serialization context if the caller
        didn't."""
        if "factions" not in self.context:
            self.context["factions"] = {}
        return in_data
