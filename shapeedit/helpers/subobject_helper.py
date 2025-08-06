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

class _SubObjectHelper:
    def __init__(self, sub_object: SubObject):
        if not isinstance(sub_object, SubObject):
            raise TypeError(f"Parameter 'sub_object' must be of type shape.SubObject, but got {type(sub_object).__name__}")
        
        self._sub_object = sub_object

    def update_geometry_info(self) -> bool:
        vertex_idxs_counts = []
        normal_idxs_counts = []

        for primitive in sub_object.primitives:
            indexed_trilist = primitive.indexed_trilist
            vertex_idxs_counts.append(len(indexed_trilist.vertex_idxs))
            normal_idxs_counts.append(int(len(indexed_trilist.vertex_idxs) / 3))

        sub_object.geometry_info.face_normals = sum(normal_idxs_counts)
        sub_object.geometry_info.trilist_indices = sum(vertex_idxs_counts)

        current_prim_total = 1

        for geometry_node in sub_object.geometry_info.geometry_nodes:
            num_primitives = geometry_node.cullable_prims.num_prims

            from_idx = current_prim_total - 1
            to_idx = current_prim_total - 1 + num_primitives

            geometry_node.cullable_prims.num_flat_sections = sum(normal_idxs_counts[from_idx : to_idx])
            geometry_node.cullable_prims.num_prim_indices = sum(vertex_idxs_counts[from_idx : to_idx])

            current_prim_total += num_primitives

    def increase_vertex_set_count(self, primitive: Primitive) -> Optional[int]:
        current_prim_total = 0
        vtx_state_idx_to_update = -1

        for idx, geometry_node in enumerate(sub_object.geometry_info.geometry_nodes):
            current_prim_total += geometry_node.cullable_prims.num_prims
            if current_prim_total > indexed_trilist._trilist_idx:
                vtx_state_idx_to_update = idx
                break

        adjust_remaining_vtx_start_idxs = False
        new_vertex_idx = None
        vtx_count_total = 0

        for idx, vertex_set in enumerate(sub_object.vertex_sets):
            if adjust_remaining_vtx_start_idxs:
                vertex_set.vtx_start_index = vtx_count_total
            
            if vertex_set.vtx_state == vtx_state_idx_to_update:
                new_count = vertex_set.vtx_count + 1
                vertex_set.vtx_count = new_count

                vtx_count_total += 1
                new_vertex_idx = vertex_set.vtx_count
                
                adjust_remaining_vtx_start_idxs = True
                
            vtx_count_total += vertex_set.vtx_count
                        
        return new_vertex_idx