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
from shapeio.shape import DistanceLevel

from .subobject_editor import _SubObjectEditor

if TYPE_CHECKING:
    from .lodcontrol_editor import _LodControlEditor


class _DistanceLevelEditor:
    def __init__(self, distance_level: DistanceLevel, _parent: "_LodControlEditor" = None):
        from .lodcontrol_editor import _LodControlEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a _LodControlEditor, not None")

        if not isinstance(distance_level, DistanceLevel):
            raise TypeError(f"Parameter 'distance_level' must be of type shape.DistanceLevel, but got {type(distance_level).__name__}")
        
        if not isinstance(_parent, _LodControlEditor):
            raise TypeError(f"Parameter '_parent' must be of type _LodControlEditor, but got {type(_parent).__name__}")

        self._distance_level = distance_level
        self._parent = _parent

    @property
    def index(self) -> int:
        """Return the index of this DistanceLevel within the parent LodControls's distance_levels list."""
        try:
            return self._parent._lod_control.distance_levels.index(self._distance_level)
        except ValueError:
            raise IndexError("DistanceLevel not found in parent's distance_levels list")
    
    @property
    def dlevel_selection(self) -> int:
        """Return the dlevel_selection of this DistanceLevel."""
        return self._distance_level.distance_level_header.dlevel_selection

    def sub_object(self, sub_object_index: int) -> _SubObjectEditor:
        if not isinstance(sub_object_index, int):
            raise TypeError(f"Parameter 'sub_object_index' must be of type int, but got {type(sub_object_index).__name__}")
        
        if not (0 <= sub_object_index < len(self._distance_level.sub_objects)):
            raise IndexError(
                f"sub_object_index {sub_object_index} out of range "
                f"(valid range: 0 to {len(self._distance_level.sub_objects) - 1})"
            )

        sub_object = self._distance_level.sub_objects[sub_object_index]
        return _SubObjectEditor(sub_object, _parent=self)
    
    def sub_objects(self) -> List[_SubObjectEditor]:
        return [
            _SubObjectEditor(sub_object, _parent=self)
            for sub_object in self._distance_level.sub_objects
        ]
