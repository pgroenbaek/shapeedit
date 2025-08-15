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

from typing import TYPE_CHECKING, List
from shapeio.shape import VertexIdx, NormalIdx, Vertex, Vector

from .vertex_editor import _VertexEditor

if TYPE_CHECKING:
    from .primitive_editor import _PrimitiveEditor


class _TriangleEditor:
    def __init__(self, vertex_idx: VertexIdx, normal_idx: NormalIdx, _parent: "_PrimitiveEditor" = None):
        from .subobject_editor import _PrimitiveEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a _PrimitiveEditor, not None")

        if not isinstance(vertex_idx, VertexIdx):
            raise TypeError(f"Parameter 'vertex_idx' must be of type shape.VertexIdx, but got {type(vertex_idx).__name__}")
        
        if not isinstance(normal_idx, NormalIdx):
            raise TypeError(f"Parameter 'normal_idx' must be of type shape.NormalIdx, but got {type(normal_idx).__name__}")
        
        if not isinstance(_parent, _PrimitiveEditor):
            raise TypeError(f"Parameter '_parent' must be of type _PrimitiveEditor, but got {type(_parent).__name__}")

        self._vertex_idx = vertex_idx
        self._normal_idx = normal_idx
        self._parent = _parent

    def vertices():
        # TODO implement
        pass

    def get_face_normal():
        # TODO implement
        pass

    def update_face_normal():
        # TODO implement
        pass