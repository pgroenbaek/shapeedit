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

from shapeio.shape import Shape

class ShapeEditor:
    def __init__(self, shape: Shape):
        self.shape = shape

    def subobject(self, lod_control_index: int, lod_dlevel: int, sub_object_index: int) -> "SubObjectEditor":
        dl = self.shape.lod_controls[lod_control_index].distance_levels[lod_dlevel]
        return SubObjectEditor(self.shape, dl.sub_objects[sub_object_index])

"""
Usage example:

shape_editor = ShapeEditor(shape)
sub_editor = shape_editor.subobject(0)

sub_editor.add_vertex(new_vertex, vtx_state_id="opaque")
sub_editor.remove_triangles(indices=[1, 4, 5])
sub_editor.validate()
"""