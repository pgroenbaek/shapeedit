"""
This file is part of ShapeEdit.

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
import copy

import shapeio


@pytest.fixture(scope="session")
def _loaded_shape():
    return shapeio.load("./tests/data/DK10f_A1tPnt5dLft.s")


@pytest.fixture(scope="function")
def global_storage(_loaded_shape):
    shape_copy = copy.deepcopy(_loaded_shape)
    return {"shape": shape_copy}
