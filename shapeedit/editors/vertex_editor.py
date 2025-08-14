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

from typing import TYPE_CHECKING
from shapeio.shape import Vertex, Point, UVPoint, Vector

if TYPE_CHECKING:
    from .subobject_editor import _SubObjectEditor


class _VertexEditor:
    def __init__(self, vertex: Vertex, _parent: "_SubObjectEditor" = None):
        from .subobject_editor import _SubObjectEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a _SubObjectEditor, not None")

        if not isinstance(vertex, Vertex):
            raise TypeError(f"Parameter 'vertex' must be of type shape.Vertex, but got {type(vertex).__name__}")
        
        if not isinstance(_parent, _SubObjectEditor):
            raise TypeError(f"Parameter '_parent' must be of type _SubObjectEditor, but got {type(_parent).__name__}")

        self._vertex = vertex
        self._parent = _parent
    
    def get_point(self) -> Point:
        pass

    def get_uv_point(self) -> UVPoint:
        pass

    def get_normal(self) -> Vector:
        pass

    def update_point(self, x: float = None, y: float = None, z: float = None) -> None:
        pass

    def update_uv_point(self, u: float = None, v: float = None) -> None:
        pass

    def update_normal(self, x: float = None, y: float = None, z: float = None) -> None:
        pass
    
    @property
    def index(self) -> int:
        """Return the index of this Vertex within the parent SubObject's vertices list."""
        try:
            return self._parent._sub_object.vertices.index(self._vertex)
        except ValueError:
            raise ValueError("Vertex not found in parent's vertices list")