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

from shapeio.shape import SubObject, Vertex, Point, UVPoint, Normal

from .editors.distancelevel_editor import _DistanceLevelEditor
from .editors.primitives_editor import _PrimitivesEditor
from .helpers.subobject_helper import _SubObjectHelper


class SubObjectEditor:
    def __init__(self, sub_object: SubObject, _parent: _DistanceLevelEditor = None):
        if _parent is None:
            raise TypeError("Parameter '_parent' cannot be None")

        if not isinstance(sub_object, SubObject):
            raise TypeError(f"Parameter 'sub_object' must be of type shape.SubObject, but got {type(sub_object).__name__}")
        
        if not isinstance(_parent, _DistanceLevelEditor):
            raise TypeError(f"Parameter '_parent' must be of type _DistanceLevelEditor, but got {type(_parent).__name__}")

        self._sub_object = sub_object
        self._parent = _parent
        self._sub_object_helper = _SubObjectHelper(sub_object)

    def distance_level(self, dlevel_selection: int) -> _LodControlEditor:
        if not isinstance(dlevel_selection, int):
            raise TypeError(f"Parameter 'dlevel_selection' must be of type int, but got {type(dlevel_selection).__name__}")

        for distance_level in self._lod_control.distance_levels:
            if distance_level.distance_level_header.dlevel_selection == dlevel_selection:
                return _DistanceLevelEditor(distance_level, _parent=self)

        raise ValueError(f"No DistanceLevel with dlevel_selection {dlevel_selection} found in this LodControl")
    
    def distance_levels(self) -> List[_DistanceLevelEditor]:
        return [
            _DistanceLevelEditor(distance_level, _parent=self)
            for distance_level in self._lod_control.distance_levels
        ]
    
    def add_vertex(self, new_point: Point, new_uv_point: UVPoint, new_normal: Normal):
        pass
    