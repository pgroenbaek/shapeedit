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

from typing import List, Callable, TypeVar

T = TypeVar('T')


def group_items_by(
    items: List[T],
    group_func: Callable[[T, T], bool]
) -> List[List[T]]:
    if not items:
        return []

    groups: List[List[T]] = []

    for item in items:
        added_to_group = False

        for group in groups:
            if group_func(group[-1], item):
                group.append(item)
                added_to_group = True
                break

        if not added_to_group:
            groups.append([item])

    return groups

