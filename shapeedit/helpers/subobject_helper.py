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

    def _update_geometry_info(self, lod_dlevel: int, subobject_idx: int) -> bool:
        current_dlevel = -1
        current_subobject_idx = -1
        current_geometry_node_idx = -1
        current_prim_total = 1
        vertexset_idx_to_update = -1

        has_updated_geometry_info = False
        has_updated_cullable_prims = False

        vertex_idxs_counts = []
        normal_idxs_counts = []

        indexed_trilists = self.get_indexed_trilists_in_subobject(lod_dlevel, subobject_idx)

        for prim_state_idx in indexed_trilists:
            for indexed_trilist in indexed_trilists[prim_state_idx]:
                vertex_idxs_counts.append(len(indexed_trilist.vertex_idxs))
                normal_idxs_counts.append(int(len(indexed_trilist.vertex_idxs) / 3))

        for line_idx, line in enumerate(self.lines):
            if "dlevel_selection (" in line:
                parts = line.split(' ')
                current_dlevel = int(parts[2])

            if current_dlevel != lod_dlevel:
                continue

            if "sub_object (" in line:
                current_subobject_idx += 1
            
            if current_subobject_idx != subobject_idx:
                continue
            
            if "geometry_info (" in line:
                parts = line.split(" ")
                parts[2] = str(sum(normal_idxs_counts))
                parts[5] = str(sum(vertex_idxs_counts))
                self.lines[line_idx] = " ".join(parts)
                has_updated_geometry_info = True

            if "cullable_prims (" in line:
                parts = line.split(" ")
                num_primitives = int(parts[2])
                from_idx = current_prim_total - 1
                to_idx = current_prim_total - 1 + num_primitives
                parts[3] = str(sum(normal_idxs_counts[from_idx : to_idx]))
                parts[4] = str(sum(vertex_idxs_counts[from_idx : to_idx]))
                self.lines[line_idx] = " ".join(parts)
                current_prim_total += num_primitives
                has_updated_cullable_prims = True
        
        return has_updated_geometry_info and has_updated_cullable_prims

    def _increase_vertex_set_count(self, lod_dlevel: int, subobject_idx: int, indexed_trilist: IndexedTrilist) -> Optional[int]:
        current_dlevel = -1
        current_subobject_idx = -1
        current_geometry_node_idx = -1
        current_prim_total = 0
        vertexset_idx_to_update = -1

        for line_idx, line in enumerate(self.lines):
            if "dlevel_selection (" in line:
                parts = line.split(' ')
                current_dlevel = int(parts[2])

            if current_dlevel != lod_dlevel:
                continue
            
            if "sub_object (" in line:
                current_subobject_idx += 1
            
            if current_subobject_idx != subobject_idx:
                continue
            
            if "geometry_node (" in line:
                current_geometry_node_idx += 1

            if "cullable_prims (" in line:
                parts = line.split()
                current_prim_total += int(parts[2])
                if current_prim_total > indexed_trilist._trilist_idx:
                    vertexset_idx_to_update = current_geometry_node_idx
                    break
        
        current_dlevel = -1
        current_subobject_idx = -1
        adjust_remaining_vertexset_idxs = False
        new_vertex_idx = None
        vertexset_count_total = 0

        for line_idx, line in enumerate(self.lines):
            if "dlevel_selection (" in line:
                parts = line.split(' ')
                current_dlevel = int(parts[2])

            if current_dlevel != lod_dlevel:
                continue
            
            if "sub_object (" in line:
                current_subobject_idx += 1
            
            if current_subobject_idx != subobject_idx:
                continue
            
            if "vertex_set (" in line:
                parts = line.split(" ")
                vertexset_idx = int(parts[2])
                vertexset_startidx = int(parts[3])
                vertexset_count = int(parts[4])

                if adjust_remaining_vertexset_idxs:
                    parts[3] = str(vertexset_count_total)
                    self.lines[line_idx] = " ".join(parts)
                
                if vertexset_idx == vertexset_idx_to_update:
                    new_count = vertexset_count + 1
                    parts[4] = str(new_count)
                    self.lines[line_idx] = " ".join(parts)
                    vertexset_count_total += 1
                    new_vertex_idx = vertexset_count
                    adjust_remaining_vertexset_idxs = True
                
                vertexset_count_total += vertexset_count
                        
        return new_vertex_idx