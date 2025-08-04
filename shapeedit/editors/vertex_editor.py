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

from shapeio.shape import Shape, Vertex

class VertexEditor:
    def __init__(self, shape: Shape, sub_object: SubObject):
        self.shape = shape
        self.lod_control_index = lod_control_index
        self.lod_dlevel = lod_dlevel
        self.sub_object_index = sub_object_index
    
    def add_texture(self, new_vertex: Vertex):
        pass
    
    def validate(self):
        assert all(0 <= v.point_index < len(self.shape.points)
                   for v in self.subobject.vertices)
        # check vertex_set bounds, prims, etc.