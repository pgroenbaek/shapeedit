"""
This file is part of ShapeMod.

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

from typing import Optional, List, Dict

import shapeio
from shapeio import shape


def remove_point(shape: shape.Shape, point: shape.Point) -> bool:
    if point not in shape.points:
        raise ValueError("Could not remove point from shape. Point given is not present in the points list of the shape.")
    # TODO Remove point
    # TODO Update vertex point indices that are greater than the removed point index
    return True

"""
def get_lod_dlevels(shape: shape.Shape) -> List[int]:
def get_prim_states(shape: shape.Shape) -> Dict[int, shape.PrimState]:
def get_prim_states_by_name(shape: shape.Shape, prim_state_name: str) -> List[shape.PrimState]:
def get_prim_state_by_idx(shape: shape.Shape, prim_state_idx: int) -> Optional[shape.PrimState]:
def get_points(shape: shape.Shape) -> Dict[int, shape.Point]:
def get_point_by_idx(shape: shape.Shape, point_idx: int) -> Optional[shape.Point]:
def set_point_value(shape: shape.Shape, point_idx: int, point: shape.Point) -> bool:
def add_point(shape: shape.Shape, point: shape.Point) -> Optional[int]:
def get_uvpoints(shape: shape.Shape) -> Dict[int, shape.UVPoint]:
def get_uvpoint_by_idx(shape: shape.Shape, uv_point_idx: int) -> Optional[UVPoint]:
def set_uvpoint_value(shape: shape.Shape, uv_point_idx: int, uv_point: UVPoint) -> bool:
def add_uvpoint(shape: shape.Shape, uv_point: UVPoint) -> Optional[int]:
def get_normals(shape: shape.Shape) -> Dict[int, Normal]:
def get_normal_by_idx(shape: shape.Shape, normal_idx: int) -> Optional[Normal]:
def set_normal_value(shape: shape.Shape, normal_idx: int, normal: Normal) -> bool:
def add_normal(shape: shape.Shape, normal: Normal) -> Optional[int]:
def get_subobject_idxs_in_lod_dlevel(shape: shape.Shape, lod_dlevel: int) -> List[int]:
def get_indexed_trilists_in_subobject(shape: shape.Shape, lod_dlevel: int, subobject_idx: int) -> Dict[int, List[IndexedTrilist]]:
def get_indexed_trilists_in_subobject_by_prim_state(shape: shape.Shape, lod_dlevel: int, subobject_idx: int, prim_state: PrimState) -> List[IndexedTrilist]:
def update_geometry_info(shape: shape.Shape, lod_dlevel: int, subobject_idx: int) -> bool:
def increase_vertexset_count(shape: shape.Shape, lod_dlevel: int, subobject_idx: int, indexed_trilist: IndexedTrilist) -> Optional[int]:
def update_indexed_trilist(shape: shape.Shape, indexed_trilist: IndexedTrilist) -> bool:
def get_vertices_in_subobject(shape: shape.Shape, lod_dlevel: int, subobject_idx: int) -> List[Vertex]:
def get_vertices_count(shape: shape.Shape, lod_dlevel: int, subobject_idx: int) -> Optional[int]:
def get_vertices_by_prim_state(shape: shape.Shape, lod_dlevel: int, prim_state: PrimState) -> List[Vertex]:
def get_vertex_in_subobject_by_idx(shape: shape.Shape, lod_dlevel: int, subobject_idx: int, vertex_idx: int) -> Optional[Vertex]:
def get_connected_vertex_idxs(shape: shape.Shape, indexed_trilist: IndexedTrilist, vertex: Vertex) -> List[int]:
def update_vertex(shape: shape.Shape, vertex: Vertex) -> bool:
def insert_triangle_between(shape: shape.Shape, indexed_trilist: IndexedTrilist, vertex1: Vertex, vertex2: Vertex, vertex3: Vertex) -> bool:
def remove_triangle_between(shape: shape.Shape, indexed_trilist: IndexedTrilist, vertex1: Vertex, vertex2: Vertex, vertex3: Vertex) -> bool:
def remove_triangles_connected_to_vertex(shape: shape.Shape, indexed_trilist: IndexedTrilist, vertex: Vertex) -> bool:
"""