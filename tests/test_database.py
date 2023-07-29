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

from datetime import datetime
from decimal import Decimal
from lethbridge.database import AtmosphereComposition
from lethbridge.database import Base
from lethbridge.database import Belt
from lethbridge.database import Body
from lethbridge.database import BodyTimestamp
from lethbridge.database import DetectedSignal
from lethbridge.database import Faction
from lethbridge.database import FactionState
from lethbridge.database import Parent
from lethbridge.database import PowerPlay
from lethbridge.database import Ring
from lethbridge.database import Signals
from lethbridge.database import System
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pytest import mark
from pytest import param


def test_metadata(mock_db_uri):
    engine = create_engine(mock_db_uri)
    Base.metadata.create_all(engine)


@mark.parametrize("x", [param("1"), param("1.000001"), param("1.0000000000001")])
def test_decimals(mock_db_uri, utilities, x):
    engine = create_engine(mock_db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    with Session.begin() as session:
        test_system_1 = System(
            id64=1,
            name="Test System 1",
            x=Decimal(x),
            y=2.0,
            z=3.0,
            date=datetime(1970, 1, 1, 0, 0, 1),
        )
        session.add(test_system_1)

    with Session.begin() as session:
        test_system_1 = session.get(System, 1)
        assert utilities.approximately(test_system_1.x, x)


def test_relationships(mock_db_uri):
    engine = create_engine(mock_db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    with Session.begin() as session:
        test_faction_1 = Faction(
            name="Test Faction 1",
            allegiance="Independent",
            government="Cooperative",
        )
        test_system_1 = System(
            id64=1,
            name="Test System 1",
            x=1.0,
            y=2.0,
            z=3.0,
            bodyCount=2,
            controllingFaction=test_faction_1,
            factions=[
                FactionState(
                    faction=test_faction_1,
                    influence=0.5,
                    state="None",
                ),
            ],
            powers=[PowerPlay(power="Zemina Torval")],
            powerState="Controlled",
            date=datetime(1970, 1, 1, 0, 0, 1),
            bodies=[
                Body(
                    id64=11,
                    bodyId=0,
                    name="Test Star",
                    type="Star",
                    belts=[
                        Belt(
                            name="Test Belt",
                            type="Rocky",
                            mass=4000000000000,
                            innerRadius=300000000000,
                            outerRadius=500000000000,
                        ),
                    ],
                    timestamps=[
                        BodyTimestamp(
                            name="distanceToArrival",
                            value=datetime(1970, 1, 1, 0, 0, 1),
                        ),
                    ],
                    stations=[],
                    updateTime=datetime(1970, 1, 1, 0, 0, 1),
                ),
                Body(
                    id64=12,
                    bodyId=1,
                    name="Test Planet",
                    type="Planet",
                    atmosphereComposition=[
                        AtmosphereComposition(name="Hydrogen", percentage=75.0),
                        AtmosphereComposition(name="Helium", percentage=25.0),
                    ],
                    signals=Signals(
                        signals=[
                            DetectedSignal(name="$SAA_SignalType_Human", quantity=1),
                        ],
                        updateTime=datetime(1970, 1, 1, 0, 0, 1),
                    ),
                    parents=[
                        Parent(name="Star", bodyId="0"),
                    ],
                    rings=[
                        Ring(
                            name="A Ring",
                            type="Icy",
                            mass=65535,
                            innerRadius=76800000,
                            outerRadius=192000000,
                        ),
                    ],
                    timestamps=[
                        BodyTimestamp(
                            name="distanceToArrival",
                            value=datetime(1970, 1, 1, 0, 0, 1),
                        ),
                        BodyTimestamp(
                            name="meanAnomaly",
                            value=datetime(1970, 1, 1, 0, 0, 1),
                        ),
                    ],
                    stations=[],
                    updateTime=datetime(1970, 1, 1, 0, 0, 1),
                ),
            ],
            stations=[],
        )
        session.add(test_system_1)
