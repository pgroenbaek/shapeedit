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

from typing import List

from shapeio.shape import Shape

from .editors.lodcontrol_editor import _LodControlEditor


class ShapeEditor:
    def __init__(self, shape: Shape):
        if not isinstance(shape, Shape):
            raise TypeError(f"Parameter 'shape' must be of type shape.Shape, but got {type(shape).__name__}")

        self._shape = shape

    def lodcontrol(self, lod_control_index: int) -> _LodControlEditor:
        if not isinstance(lod_control_index, int):
            raise TypeError(f"Parameter 'lod_control_index' must be of type int, but got {type(lod_control_index).__name__}")
        
        if not (0 <= lod_control_index < len(self._shape.lod_controls)):
            raise IndexError(
                f"lod_control_index {lod_control_index} out of range "
                f"(valid range: 0 to {len(self._shape.lod_controls) - 1})"
            )

        lod_control = self._shape.lod_controls[lod_control_index]
        return _LodControlEditor(lod_control, _parent=self)

    def lodcontrols(self) -> List[_LodControlEditor]:
        return [
            _LodControlEditor(lod_control, _parent=self)
            for lod_control in self._shape.lod_controls
        ]