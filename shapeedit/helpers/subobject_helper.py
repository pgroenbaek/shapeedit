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

from typing import Optional
from shapeio.shape import SubObject, Primitive


class _SubObjectHelper:
    """
    Internal helper class for a `SubObject`.

    This class is used internally within `_SubObjectEditor` to manage
    low-level SubObject data, such as geometry info and vertex sets.
    It **should not be instantiated or used directly** by
    external code.

    Args:
        sub_object (SubObject): The SubObject to wrap.

    Raises:
        TypeError: If `sub_object` is not a `SubObject`.
    """

    def __init__(self, sub_object: SubObject):
        """
        Initializes the internal `_SubObjectHelper`.

        Do not instantiate this class directly; it is intended for internal use
        within `_SubObjectEditor` and its children editors.

        Args:
            sub_object (SubObject): The SubObject to wrap and manage.

        Raises:
            TypeError: If `sub_object` is not a `SubObject` instance.
        """
        if not isinstance(sub_object, SubObject):
            raise TypeError(f"Parameter 'sub_object' must be of type shape.SubObject, but got {type(sub_object).__name__}")
        
        self._sub_object = sub_object

    def update_geometry_info(self):
        """
        Recalculates and updates geometry information for the sub-object.

        Updates `geometry_info` and `cullable_prims` based on the
        current primitives and triangle lists, including:
            - Total number of face normals
            - Total number of trilist indices
            - Primitive-level counts in geometry nodes
        """

        # Gather vertex and face counts based on trilist data
        vertex_idxs_counts = []
        normal_idxs_counts = []

        for primitive in sub_object.primitives:
            indexed_trilist = primitive.indexed_trilist
            vertex_idxs_counts.append(len(indexed_trilist.vertex_idxs))
            normal_idxs_counts.append(int(len(indexed_trilist.vertex_idxs) / 3))

        # Update values within geometry_info
        sub_object.geometry_info.face_normals = sum(normal_idxs_counts)
        sub_object.geometry_info.trilist_indices = sum(vertex_idxs_counts)

        # Update values within cullable_prims
        current_prim_idx = 0

        for geometry_node in sub_object.geometry_info.geometry_nodes:
            num_primitives = geometry_node.cullable_prims.num_prims
            from_idx = current_prim_idx
            to_idx = current_prim_idx + num_primitives

            geometry_node.cullable_prims.num_flat_sections = sum(normal_idxs_counts[from_idx:to_idx])
            geometry_node.cullable_prims.num_prim_indices = sum(vertex_idxs_counts[from_idx:to_idx])

            current_prim_idx += num_primitives

    def expand_vertexset(self, primitive: Primitive) -> Optional[int]:
        """
        Expands the vertex set counts to make way for
        adding a new vertex to the specified primitive.

        Finds the vertex state index corresponding to the primitive,
        increments the vertex count, and adjusts start indices in
        the vertex sets.

        Args:
            primitive (Primitive): The primitive whose vertex set should be expanded.

        Returns:
            Optional[int]: The new vertex index in the expanded vertex set,
            or `None` if no update was performed.
        """

        # Find the vertex state index to update
        total_prims = 0
        vtx_state_idx_to_update = -1

        for idx, node in enumerate(sub_object.geometry_info.geometry_nodes):
            total_prims += node.cullable_prims.num_prims
            if total_prims > indexed_trilist._trilist_idx:
                vtx_state_idx_to_update = idx
                break

        # Update the vertex count and adjust start indices
        new_vertex_idx = None
        total_vertex_count = 0
        update_start_indices = False

        for vertex_set in sub_object.vertex_sets:
            if update_start_indices:
                vertex_set.vtx_start_index = total_vertex_count

            if vertex_set.vtx_state == vtx_state_idx_to_update:
                vertex_set.vtx_count += 1
                total_vertex_count += 1
                update_start_indices = True
                new_vertex_idx = vertex_set.vtx_count

            total_vertex_count += vertex_set.vtx_count

        return new_vertex_idx