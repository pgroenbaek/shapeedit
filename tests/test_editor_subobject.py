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

import pytest

from shapeedit import ShapeEditor
from shapeedit.editors.primitive_editor import _PrimitiveEditor
from shapeedit.editors.vertex_editor import _VertexEditor


def test_subobject_editor_primitives(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    primitives = sub_object.primitives()
    assert len(primitives) == 22


def test_subobject_editor_primitive_by_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    primitive = sub_object.primitive(0)
    assert isinstance(primitive, _PrimitiveEditor)


def test_subobject_editor_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    assert sub_object.index == 0


@pytest.mark.parametrize("bad_value", [
    22, -1, 300, 1337
])
def test_subobject_editor_primitive_by_index_raises(global_storage, bad_value):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    sub_object = ShapeEditor(shape).lod_control(0).distance_level(200).sub_object(0)

    with pytest.raises(IndexError):
        sub_object.primitive(bad_value)


def test_subobject_editor_vertices(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    vertices = sub_object.vertices()
    assert len(vertices) == 7427


def test_subobject_editor_vertex_by_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    vertex = sub_object.vertex(0)
    assert isinstance(vertex, _VertexEditor)


@pytest.mark.parametrize("bad_value", [
    7427, -1, 13337
])
def test_subobject_editor_vertex_by_index_raises(global_storage, bad_value):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    primitive = ShapeEditor(shape).lod_control(0).distance_level(200).sub_object(0)

    with pytest.raises(IndexError):
        primitive.vertex(bad_value)