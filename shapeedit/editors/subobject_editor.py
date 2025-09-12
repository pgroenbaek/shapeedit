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

from typing import TYPE_CHECKING, List, Optional
from shapeio.shape import SubObject, Vertex

from .primitive_editor import _PrimitiveEditor
from .vertex_editor import _VertexEditor
from ..helpers.subobject_helper import _SubObjectHelper

if TYPE_CHECKING:
    from .distancelevel_editor import _DistanceLevelEditor


class _SubObjectEditor:
    def __init__(self, sub_object: SubObject, _parent: "_DistanceLevelEditor" = None):
        from .distancelevel_editor import _DistanceLevelEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a _DistanceLevelEditor, not None")

        if not isinstance(sub_object, SubObject):
            raise TypeError(f"Parameter 'sub_object' must be of type shape.SubObject, but got {type(sub_object).__name__}")
        
        if not isinstance(_parent, _DistanceLevelEditor):
            raise TypeError(f"Parameter '_parent' must be of type _DistanceLevelEditor, but got {type(_parent).__name__}")

        self._sub_object = sub_object
        self._parent = _parent
        self._sub_object_helper = _SubObjectHelper(sub_object)
    
    @property
    def index(self) -> int:
        """Return the index of this SubObject within the parent DistanceLevel's sub_objects list."""
        try:
            return self._parent._distance_level.sub_objects.index(self._sub_object)
        except IndexError:
            raise IndexError("SubObject not found in parent's sub_objects list")

    def primitive(self, primitive_index: int) -> _PrimitiveEditor:
        if not isinstance(primitive_index, int):
            raise TypeError(f"Parameter 'primitive_index' must be of type int, but got {type(primitive_index).__name__}")
        
        if not (0 <= primitive_index < len(self._sub_object.primitives)):
            raise IndexError(
                f"primitive_index {primitive_index} out of range "
                f"(valid range: 0 to {len(self._sub_object.primitives) - 1})"
            )

        primitive = self._sub_object.primitives[primitive_index]
        return _PrimitiveEditor(primitive, _parent=self)
    
    def primitives(self, prim_state_index: Optional[int] = None, prim_state_name: Optional[str] = None) -> List[_PrimitiveEditor]:
        # TODO also filter based on prim_state_index and prim_state_name
        return [
            _PrimitiveEditor(primitive, _parent=self)
            for primitive in self._sub_object.primitives
        ]
    
    def vertex(self, vertex_index: int) -> _VertexEditor:
        if not isinstance(vertex_index, int):
            raise TypeError(f"Parameter 'vertex_index' must be of type int, but got {type(vertex_index).__name__}")

        if not (0 <= vertex_index < len(self._sub_object.vertices)):
            raise IndexError(
                f"vertex_index {vertex_index} out of range "
                f"(valid range: 0 to {len(self._sub_object.vertices) - 1})"
            )

        vertex = self._sub_object.vertices[vertex_index]
        return _VertexEditor(vertex, _parent=self)
    
    def vertices(self) -> List[_VertexEditor]:
        return [
            _VertexEditor(vertex, _parent=self)
            for vertex in self._sub_object.vertices
        ]