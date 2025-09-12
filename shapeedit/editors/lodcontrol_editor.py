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
from shapeio.shape import LodControl

from .distancelevel_editor import _DistanceLevelEditor

if TYPE_CHECKING:
    from .shape_editor import ShapeEditor


class _LodControlEditor:
    def __init__(self, lod_control: LodControl, _parent: "ShapeEditor" = None):
        from .shape_editor import ShapeEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a ShapeEditor, not None")

        if not isinstance(lod_control, LodControl):
            raise TypeError(f"Parameter 'lod_control' must be of type shape.LodControl, but got {type(lod_control).__name__}")
        
        if not isinstance(_parent, ShapeEditor):
            raise TypeError(f"Parameter '_parent' must be of type ShapeEditor, but got {type(_parent).__name__}")

        self._lod_control = lod_control
        self._parent = _parent

    @property
    def index(self) -> int:
        """Return the index of this LodControl within the parent Shape's lod_controls list."""
        try:
            return self._parent._shape.lod_controls.index(self._lod_control)
        except IndexError:
            raise IndexError("LodControl not found in parent's lod_controls list")
    
    def distance_level(self, dlevel_selection: int) -> _DistanceLevelEditor:
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