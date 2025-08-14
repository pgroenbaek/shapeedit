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
from shapeio.shape import Primitive, Vertex

from .vertex_editor import _VertexEditor

if TYPE_CHECKING:
    from .subobject_editor import _SubObjectEditor


class _PrimitiveEditor:
    def __init__(self, primitive: Primitive, _parent: "_SubObjectEditor" = None):
        from .subobject_editor import _SubObjectEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' cannot be None")

        if not isinstance(primitive, Primitive):
            raise TypeError(f"Parameter 'primitive' must be of type shape.Primitive, but got {type(primitive).__name__}")
        
        if not isinstance(_parent, _SubObjectEditor):
            raise TypeError(f"Parameter '_parent' must be of type _SubObjectEditor, but got {type(_parent).__name__}")

        self._primitive = primitive
        self._parent = _parent

    def vertex(self, vertex_index: int) -> _VertexEditor:
        if not isinstance(sub_object_index, int):
            raise TypeError(f"Parameter 'vertex_index' must be of type int, but got {type(vertex_index).__name__}")
        
        if not (0 <= vertex_index < len(self._primitive.vertices)):
            raise IndexError(
                f"vertex_index {vertex_index} out of range "
                f"(valid range: 0 to {len(self._primitive.vertices) - 1})"
            )

        vertex = self._primitive.vertices[vertex_index]
        return _VertexEditor(vertex, _parent=self)
    
    def vertices(self) -> List[_VertexEditor]:
        return [
            _VertexEditor(vertex, _parent=self)
            for vertex in self._primitive.vertices
        ]
    
    def get_matrix(self):
        pass
    
    def insert_triangle(self, vertex1: Vertex, vertex2: Vertex, vertex3: Vertex):
        pass

    def remove_triangle(self, vertex1: Vertex, vertex2: Vertex, vertex3: Vertex):
        pass

    def remove_triangles_connected_to(self, new_vertex: Vertex):
        pass
    
    @property
    def index(self) -> int:
        """Return the index of this Primitive within the parent SubObject's primitives list."""
        try:
            return self._parent._sub_object.primitives.index(self._primitive)
        except ValueError:
            raise ValueError("Primitive not found in parent's primitives list")