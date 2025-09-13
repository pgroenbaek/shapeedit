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

    @property
    def index(self) -> int:
        """Return the index of this triangle within the parent Primitive's vertex_idxs list."""
        try:
            return self._parent._primitive.indexed_trilist.vertex_idxs.index(self._vertex_idx)
        except ValueError:
            raise IndexError("Triangle not found in parent's vertex_idxs list")

    @property
    def face_normal(self) -> Vector:
        shape = self._parent._parent._parent._parent._parent._shape
        normal_idx = self._normal_idx.index

        if not (normal_idx < len(shape.normals)):
            raise IndexError("Normal not found in shape's normals list")
        
        return shape.normals[normal_idx]

    @face_normal.setter
    def face_normal(self, face_normal: Vector):
        shape = self._parent._parent._parent._parent._parent._shape

        if not isinstance(face_normal, Vector):
            raise TypeError(f"Parameter 'face_normal' must be of type shape.Vector, but got {type(face_normal).__name__}")

        if face_normal in shape.normals:
            normal_idx = shape.normals.index(face_normal)
        else:
            shape.normals.append(face_normal)
            normal_idx = len(shape.normals) - 1

        self._normal_idx.index = normal_idx

    def vertices(self) -> List[_VertexEditor]:
        sub_object = self._parent._parent._sub_object

        vertex1_idx = self._vertex_idx.vertex1_index
        vertex2_idx = self._vertex_idx.vertex2_index
        vertex3_idx = self._vertex_idx.vertex3_index

        for vertex_idx in [vertex1_idx, vertex2_idx, vertex3_idx]:
            if not (vertex_idx < len(sub_object.vertices)):
                raise IndexError(
                    f"Vertex index {vertex_idx} not found in SubObject's vertices list"
                )

        vertex1 = sub_object.vertices[self._vertex_idx.vertex1_index]
        vertex2 = sub_object.vertices[self._vertex_idx.vertex2_index]
        vertex3 = sub_object.vertices[self._vertex_idx.vertex3_index]

        return [
            _VertexEditor(vertex1, _parent=self._parent._parent),
            _VertexEditor(vertex2, _parent=self._parent._parent),
            _VertexEditor(vertex3, _parent=self._parent._parent),
        ]