"""
This file is part of ShapeIO.

Copyright (C) 2025 Peter Grønbæk Andersen <peter@grnbk.io>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import pytest

import shapemod
from shapeio.shape import Point


@pytest.fixture
def serializer():
    return _ColourSerializer()


def test_serialize_colour(serializer):
    colour = Colour(1.0, 2.2, 3.2, 4.5)
    assert serializer.serialize(colour) == "colour ( 1 2.2 3.2 4.5 )"
