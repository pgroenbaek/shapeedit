"""
This file is part of ShapeMod.

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

import codecs
import subprocess
from typing import Optional

import shapeio
from shapeio import shape


def remove_point(shape: shape.Shape, point: shape.Point) -> bool:
    if point not in shape.points:
        raise ValueError("Could not remove point from shape. Point given is not present in the points list of the shape.")
    # TODO Remove point
    # TODO Update vertex point indices that are greater than the removed point index
    return True