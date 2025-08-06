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

from shapeio.shape import Vertex, Point, UVPoint, Normal

from .editors.primitives_editor import _PrimitiveEditor


class VertexEditor:
    def __init__(self, vertex: Vertex, _parent: _PrimitiveEditor = None):
        if _parent is None:
            raise TypeError("Parameter '_parent' cannot be None")

        if not isinstance(vertex, Vertex):
            raise TypeError(f"Parameter 'vertex' must be of type shape.Vertex, but got {type(vertex).__name__}")
        
        if not isinstance(_parent, _PrimitiveEditor):
            raise TypeError(f"Parameter '_parent' must be of type _PrimitiveEditor, but got {type(_parent).__name__}")

        self._vertex = vertex
        self._parent = _parent
    
    def update_point(self, x: float = None, y: float = None, z: float = None):
        pass

    def update_uv_point(self, u: float = None, v: float = None):
        pass

    def update_normal(self, x: float = None, y: float = None, z: float = None):
        pass
    