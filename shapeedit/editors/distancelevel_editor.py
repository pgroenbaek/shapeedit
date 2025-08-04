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

from shapeio.shape import DistanceLevel

from .editors.subobject_editor import _SubObjectEditor


class _DistanceLevelEditor:
    def __init__(self, distance_level: DistanceLevel, _parent: ShapeEditor = None):
        if _parent is None:
            raise TypeError("Parameter '_parent' cannot be None")

        if not isinstance(distance_level, DistanceLevel):
            raise TypeError(f"Parameter 'distance_level' must be of type shape.DistanceLevel, but got {type(distance_level).__name__}")
        
        if not isinstance(_parent, ShapeEditor):
            raise TypeError(f"Parameter '_parent' must be of type ShapeEditor, but got {type(_parent).__name__}")

        self._distance_level = distance_level
        self._parent = _parent

    def subobject(self, sub_object_index: int) -> _SubObjectEditor:
        if not isinstance(sub_object_index, int):
            raise TypeError(f"Parameter 'sub_object_index' must be of type int, but got {type(sub_object_index).__name__}")
        
        if not (0 <= sub_object_index < len(self._distance_level.sub_objects)):
            raise IndexError(
                f"sub_object_index {sub_object_index} out of range "
                f"(valid range: 0 to {len(self._distance_level.sub_objects) - 1})"
            )

        sub_object = self._distance_level.sub_objects[sub_object_index]
        return _SubObjectEditor(sub_object, _parent=self)
    
    # def validate(self):
    #     assert all(0 <= v.point_index < len(self.shape.points)
    #                for v in self.subobject.vertices)
    #     # check vertex_set bounds, prims, etc.