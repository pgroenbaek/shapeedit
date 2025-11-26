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

import numpy as np
from typing import List
from shapeio import shape


def remap_point(
    point: shape.Point,
    from_matrix: shape.Matrix,
    to_matrix: shape.Matrix
) -> shape.Point:
    """
    Remaps a 3D point from one coordinate space to another using transformation matrices.

    This function transforms a point that is defined in the coordinate system of 
    `from_matrix` into the coordinate system defined by `to_matrix`.

    Args:
        point (shape.Point): The point to be transformed.
        from_matrix (shape.Matrix): The original coordinate system (source transform).
        to_matrix (shape.Matrix): The target coordinate system (destination transform).

    Returns:
        shape.Point: The point transformed into the new coordinate system.
    """
    old_matrix = from_matrix.to_numpy().astype(np.float32)
    new_matrix = to_matrix.to_numpy().astype(np.float32)

    R_old = old_matrix[:3, :]
    t_old = old_matrix[3, :]
    R_new = new_matrix[:3, :]
    t_new = new_matrix[3, :]

    p = np.array([point.x, point.y, point.z], dtype=np.float32)
    p_world = p @ R_old + t_old
    p_new = (p_world - t_new) @ np.linalg.inv(R_new)

    return shape.Point.from_numpy(p_new.astype(float))


def remap_normal(
    normal: shape.Vector,
    from_matrix: shape.Matrix,
    to_matrix: shape.Matrix
) -> shape.Vector:
    """
    Remaps a 3D normal vector from one coordinate space to another using transformation matrices.

    This function transforms a normal vector, taking into account the non-uniform scaling
    or shearing that may be present in the transformation. It uses the inverse transpose
    of the linear part of the transformation matrix to properly transform the normal.

    Args:
        normal (shape.Vector): The normal vector to be transformed.
        from_matrix (shape.Matrix): The original coordinate system (source transform).
        to_matrix (shape.Matrix): The target coordinate system (destination transform).

    Returns:
        shape.Vector: The normal vector transformed into the new coordinate system.
    """
    old_matrix = from_matrix.to_numpy().astype(np.float32)
    new_matrix = to_matrix.to_numpy().astype(np.float32)

    R_old = old_matrix[:3, :]
    R_new = new_matrix[:3, :]

    linear = np.linalg.inv(R_new) @ R_old
    normal_matrix = np.linalg.inv(linear).T

    n = np.array([normal.x, normal.y, normal.z], dtype=np.float32)
    n_new = normal_matrix @ n
    n_new /= np.linalg.norm(n_new)

    return shape.Vector.from_numpy(n_new.astype(float))