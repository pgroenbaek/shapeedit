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
from shapeio.shape import Primitive, Vertex, Point, UVPoint, Vector, Matrix

from .vertex_editor import _VertexEditor

if TYPE_CHECKING:
    from .subobject_editor import _SubObjectEditor


class _PrimitiveEditor:
    def __init__(self, primitive: Primitive, _parent: "_SubObjectEditor" = None):
        from .subobject_editor import _SubObjectEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a _SubObjectEditor, not None")

        if not isinstance(primitive, Primitive):
            raise TypeError(f"Parameter 'primitive' must be of type shape.Primitive, but got {type(primitive).__name__}")
        
        if not isinstance(_parent, _SubObjectEditor):
            raise TypeError(f"Parameter '_parent' must be of type _SubObjectEditor, but got {type(_parent).__name__}")

        self._primitive = primitive
        self._parent = _parent

    def vertices(self) -> List[_VertexEditor]:
        parent_vertices = self._parent._sub_object.vertices
        seen = set()
        unique_ordered_indices = []

        for vertex_idx in self._primitive.indexed_trilist.vertex_idxs:
            for idx in (vertex_idx.vertex1_index, vertex_idx.vertex2_index, vertex_idx.vertex3_index):
                if idx not in seen:
                    seen.add(idx)
                    unique_ordered_indices.append(idx)

        return [_VertexEditor(parent_vertices[idx], _parent=self._parent) for idx in unique_ordered_indices]
    
    def get_matrix(self) -> Matrix:
        shape = self._parent._parent._parent._parent._shape
        prim_state_idx = self._primitive.prim_state_index
        vtx_state_idx = shape.prim_states[prim_state_idx].vtx_state_index
        matrix_idx = shape.vtx_states[vtx_state_idx].matrix_index
        return shape.matrices[matrix_idx]

    def add_vertex(self, new_point: Point, new_uv_point: UVPoint, new_normal: Vector):
        # TODO implement
        pass
    
    def insert_triangle(self, vertex1: Vertex, vertex2: Vertex, vertex3: Vertex):
        # TODO implement
        pass

    def remove_triangle(self, vertex1: Vertex, vertex2: Vertex, vertex3: Vertex):
        # TODO implement
        pass

    def remove_triangles_connected_to(self, new_vertex: Vertex):
        # TODO implement
        pass
    
    @property
    def index(self) -> int:
        """Return the index of this Primitive within the parent SubObject's primitives list."""
        try:
            return self._parent._sub_object.primitives.index(self._primitive)
        except ValueError:
            raise ValueError("Primitive not found in parent's primitives list")