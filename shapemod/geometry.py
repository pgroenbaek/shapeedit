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

import numpy as np
from typing import List

from shapeio import shape


def calculate_point_centroid(
    points: List[shape.Point]
) -> shape.Point:

    positions = [p.to_numpy() for p in points]

    centroid = np.mean(positions, axis=0)

    return shape.Point.from_numpy(centroid)


def calculate_point_midpoint(
    point1: shape.Point,
    point2: shape.Point
) -> shape.Point:

    midpoint = (point1.to_numpy() + point2.to_numpy()) / 2

    return shape.Point.from_numpy(midpoint)


def calculate_uvpoint_midpoint(
    uv_point1: shape.UVPoint,
    uv_point2: shape.UVPoint
) -> shape.UVPoint:

    midpoint = (uv_point1.to_numpy() + uv_point2.to_numpy()) / 2

    return shape.UVPoint.from_numpy(midpoint)
    

def calculate_face_normal(
    point1: shape.Point,
    point2: shape.Point,
    point3: shape.Point
) -> shape.Vector:

    edge1 = point2.to_numpy() - point1.to_numpy()
    edge2 = point3.to_numpy() - point1.to_numpy()

    normal = np.cross(edge1, edge2)

    if np.linalg.norm(normal) > 1e-10:
        normal /= np.linalg.norm(normal)
    else:
        normal = np.zeros_like(normal)

    normal = np.round(normal, 4)

    return shape.Vector.from_numpy(normal)


def calculate_vertex_normal(
    point: shape.Point,
    connected_points: List[shape.Point]
) -> shape.Vector:

    vertex_normal_sum = np.zeros(3)

    if len(connected_points) < 2:
        return shape.Vector(0, 0, 0)
    
    for i in range(len(connected_points) - 1):
        edge1 = connected_points[i].to_numpy() - point.to_numpy()
        edge2 = connected_points[i + 1].to_numpy() - point.to_numpy()

        normal = np.cross(edge1, edge2)

        if np.linalg.norm(normal) > 1e-10:
            normal /= np.linalg.norm(normal)
        else:
            normal = np.zeros_like(normal)

        normal = np.round(normal, 4)
        vertex_normal_sum += normal
    
    return shape.Vector.from_numpy(vertex_normal_sum)

