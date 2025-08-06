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

from shapeedit import ShapeEditor


def test_shape_has_lods(global_storage):
    shape = global_storage["shape"]
    editor = ShapeEditor(shape)

    lods = editor.all_lodcontrols()
    assert len(lods) > 0, "Shape should have at least one LOD control"


def test_add_vertex_to_first_subobject(global_storage):
    shape = global_storage["shape"]
    editor = ShapeEditor(shape)

    # Assume there's at least one LOD, one dlevel, and one subobject
    lod_editor = editor.lodcontrol(0)
    dlevel_editor = lod_editor.distancelevels()[0]
    subobj_editor = dlevel_editor.subobject(0)

    new_vertex = ...  # your vertex creation logic here
    original_count = len(shape.points)

    subobj_editor.add_vertex(new_vertex)

    assert len(shape.points) == original_count + 1
