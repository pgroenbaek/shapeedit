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

from .triangle_editor import _TriangleEditor
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
    
    @property
    def index(self) -> int:
        """Return the index of this Primitive within the parent SubObject's primitives list."""
        try:
            return self._parent._sub_object.primitives.index(self._primitive)
        except ValueError:
            raise IndexError("Primitive not found in parent's primitives list")

    @property
    def matrix(self) -> Matrix:
        shape = self._parent._parent._parent._parent._shape
        prim_state_idx = self._primitive.prim_state_index
        vtx_state_idx = shape.prim_states[prim_state_idx].vtx_state_index
        matrix_idx = shape.vtx_states[vtx_state_idx].matrix_index
        return shape.matrices[matrix_idx]

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
    
    def triangle(self, triangle_index: int) -> _TriangleEditor:
        if not isinstance(triangle_index, int):
            raise TypeError(f"Parameter 'triangle_index' must be of type int, but got {type(triangle_index).__name__}")

        indexed_trilist = self._primitive.indexed_trilist

        if not (0 <= triangle_index < len(indexed_trilist.vertex_idxs)):
            raise IndexError(
                f"triangle_index {triangle_index} out of range "
                f"(valid range: 0 to {len(indexed_trilist.vertex_idxs) - 1})"
            )
        
        if not (0 <= triangle_index < len(indexed_trilist.normal_idxs)):
            raise IndexError(
                f"triangle_index {triangle_index} out of range "
                f"(valid range: 0 to {len(indexed_trilist.normal_idxs) - 1})"
            )

        vertex_idx = indexed_trilist.vertex_idxs[triangle_index]
        normal_idx = indexed_trilist.normal_idxs[triangle_index]
        return _TriangleEditor(vertex_idx, normal_idx, _parent=self)
    
    def triangles(self) -> List[_TriangleEditor]:
        indexed_trilist = self._primitive.indexed_trilist
        return [
            _TriangleEditor(vertex_idx, normal_idx, _parent=self)
            for vertex_idx, normal_idx in zip(indexed_trilist.vertex_idxs, indexed_trilist.normal_idxs)
        ]

    def add_vertex(self, new_point: Point, new_uv_point: UVPoint, new_normal: Vector) -> _VertexEditor:
        shape = self._parent._parent._parent._parent._shape
        # TODO implement
        pass
    
    def insert_triangle(self, vertex1: _VertexEditor, vertex2: _VertexEditor, vertex3: _VertexEditor) -> _TriangleEditor:
        shape = self._parent._parent._parent._parent._shape

        if not isinstance(vertex1, _VertexEditor):
            raise TypeError(f"Parameter 'vertex1' must be of type _VertexEditor, but got {type(vertex1).__name__}")
        if not isinstance(vertex2, _VertexEditor):
            raise TypeError(f"Parameter 'vertex2' must be of type _VertexEditor, but got {type(vertex2).__name__}")
        if not isinstance(vertex3, _VertexEditor):
            raise TypeError(f"Parameter 'vertex3' must be of type _VertexEditor, but got {type(vertex3).__name__}")

        if not self._parent._sub_object is vertex1._parent._sub_object:
            raise ValueError("Parameter 'vertex1' is not from the same sub-object")
        if not self._parent._sub_object is vertex2._parent._sub_object:
            raise ValueError("Parameter 'vertex2' is not from the same sub-object")
        if not self._parent._sub_object is vertex3._parent._sub_object:
            raise ValueError("Parameter 'vertex3' is not from the same sub-object")
        
        # TODO implement
        pass

    def remove_triangle(self, vertex1: _VertexEditor, vertex2: _VertexEditor, vertex3: _VertexEditor):
        shape = self._parent._parent._parent._parent._shape

        if not isinstance(vertex1, _VertexEditor):
            raise TypeError(f"Parameter 'vertex1' must be of type _VertexEditor, but got {type(vertex1).__name__}")
        if not isinstance(vertex2, _VertexEditor):
            raise TypeError(f"Parameter 'vertex2' must be of type _VertexEditor, but got {type(vertex2).__name__}")
        if not isinstance(vertex3, _VertexEditor):
            raise TypeError(f"Parameter 'vertex3' must be of type _VertexEditor, but got {type(vertex3).__name__}")

        if not self._parent._sub_object is vertex1._parent._sub_object:
            raise ValueError("Parameter 'vertex1' is not from the same sub-object")
        if not self._parent._sub_object is vertex2._parent._sub_object:
            raise ValueError("Parameter 'vertex2' is not from the same sub-object")
        if not self._parent._sub_object is vertex3._parent._sub_object:
            raise ValueError("Parameter 'vertex3' is not from the same sub-object")

        # TODO implement
        pass

    def remove_triangles_connected_to(self, vertex: _VertexEditor):
        shape = self._parent._parent._parent._parent._shape

        if not isinstance(vertex, _VertexEditor):
            raise TypeError(f"Parameter 'vertex' must be of type _VertexEditor, but got {type(vertex).__name__}")

        if not self._parent._sub_object is vertex._parent._sub_object:
            raise ValueError("Parameter 'vertex' is not from the same sub-object")
        
        # TODO implement
        pass