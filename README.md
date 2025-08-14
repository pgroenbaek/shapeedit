# shapeedit

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/pgroenbaek/shapeedit?style=flat&label=Latest%20Version)](https://github.com/pgroenbaek/shapeedit/releases)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License GNU GPL v3](https://img.shields.io/badge/License-%20%20GNU%20GPL%20v3%20-lightgrey?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NDAgNTEyIj4KICA8IS0tIEZvbnQgQXdlc29tZSBGcmVlIDYuNy4yIGJ5IEBmb250YXdlc29tZSAtIGh0dHBzOi8vZm9udGF3ZXNvbWUuY29tIExpY2Vuc2UgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbS9saWNlbnNlL2ZyZWUgQ29weXJpZ2h0IDIwMjUgRm9udGljb25zLCBJbmMuIC0tPgogIDxwYXRoIGZpbGw9IndoaXRlIiBkPSJNMzg0IDMybDEyOCAwYzE3LjcgMCAzMiAxNC4zIDMyIDMycy0xNC4zIDMyLTMyIDMyTDM5OC40IDk2Yy01LjIgMjUuOC0yMi45IDQ3LjEtNDYuNCA1Ny4zTDM1MiA0NDhsMTYwIDBjMTcuNyAwIDMyIDE0LjMgMzIgMzJzLTE0LjMgMzItMzIgMzJsLTE5MiAwLTE5MiAwYy0xNy43IDAtMzItMTQuMy0zMi0zMnMxNC4zLTMyIDMyLTMybDE2MCAwIDAtMjk0LjdjLTIzLjUtMTAuMy00MS4yLTMxLjYtNDYuNC01Ny4zTDEyOCA5NmMtMTcuNyAwLTMyLTE0LjMtMzItMzJzMTQuMy0zMiAzMi0zMmwxMjggMGMxNC42LTE5LjQgMzcuOC0zMiA2NC0zMnM0OS40IDEyLjYgNjQgMzJ6bTU1LjYgMjg4bDE0NC45IDBMNTEyIDE5NS44IDQzOS42IDMyMHpNNTEyIDQxNmMtNjIuOSAwLTExNS4yLTM0LTEyNi03OC45Yy0yLjYtMTEgMS0yMi4zIDYuNy0zMi4xbDk1LjItMTYzLjJjNS04LjYgMTQuMi0xMy44IDI0LjEtMTMuOHMxOS4xIDUuMyAyNC4xIDEzLjhsOTUuMiAxNjMuMmM1LjcgOS44IDkuMyAyMS4xIDYuNyAzMi4xQzYyNy4yIDM4MiA1NzQuOSA0MTYgNTEyIDQxNnpNMTI2LjggMTk1LjhMNTQuNCAzMjBsMTQ0LjkgMEwxMjYuOCAxOTUuOHpNLjkgMzM3LjFjLTIuNi0xMSAxLTIyLjMgNi43LTMyLjFsOTUuMi0xNjMuMmM1LTguNiAxNC4yLTEzLjggMjQuMS0xMy44czE5LjEgNS4zIDI0LjEgMTMuOGw5NS4yIDE2My4yYzUuNyA5LjggOS4zIDIxLjEgNi43IDMyLjFDMjQyIDM4MiAxODkuNyA0MTYgMTI2LjggNDE2UzExLjcgMzgyIC45IDMzNy4xeiIvPgo8L3N2Zz4=&logoColor=%23ffffff)](/LICENSE)

This Python module provides a wrapper around the shape data structure with operations for modifying existing MSTS/ORTS shape files that keeps the shape error-free and usable in MSTS and Open Rails.

At this stage, only a limited set of operations is implemented, such as adding vertices, connecting them with triangles, and removing triangles. If you need additional functionality, feel free to request it by creating an issue or submitting a pull request.

List of companion modules:
- [shapeio](https://github.com/pgroenbaek/shapeio) - offers functions to convert shapes between structured text format and Python objects.
- [trackshape-utils](https://github.com/pgroenbaek/trackshape-utils) - offers additional utilities for working with track shapes.

## Installation

### Install from PyPI

```sh
pip install --upgrade shapeedit
```

### Install from wheel

If you have downloaded a `.whl` file from the [Releases](https://github.com/pgroenbaek/shapeedit/releases) page, install it with:

```sh
pip install path/to/shapeedit-<version>‑py3‑none‑any.whl
```

Replace `<version>` with the actual version number in the filename. For example:

```sh
pip install path/to/shapeedit-0.5.0b0-py3-none-any.whl
```

### Install from source

```sh
git clone https://github.com/pgroenbaek/shapeedit.git
pip install --upgrade ./shapeedit
```

## Usage

```python
import shapeio
from shapeio.shape import Point, UVPoint, Vector
from shapeedit import ShapeEditor

my_shape = shapeio.load("./path/to/example.s")

shape_editor = ShapeEditor(my_shape)

sub_object = shape_editor.lod_control(0).distance_level(200).sub_object(0)

for vertex in sub_object.vertices():
    vertex.update_point(x=0.0, y=0.0, z=0.0)
    vertex.update_uv_point(u=0.0, v=0.0)
    vertex.update_normal(x=0.0, y=0.0, z=0.0)

shapeio.dump(my_shape, "./path/to/output.s")
```


```python
import shapeio
from shapeio.shape import Point, UVPoint, Vector
from shapeedit import ShapeEditor

my_shape = shapeio.load("./path/to/example.s")

shape_editor = ShapeEditor(my_shape)

for lod_control in shape_editor.lod_controls():
    for distance_level in lod_control.distance_levels():
        for sub_object in distance_level.sub_objects():
            for primitive in sub_object.primitives(prim_state_idx=22):
                new_point = Point(0.0, 0.0, 0.0)
                new_uv_point = UVPoint(0.0, 0.0)
                new_normal = Vector(0.0, 0.0, 0.0)

                new_vertex1 = primitive.add_vertex(new_point, new_uv_point, new_normal)
                new_vertex2 = primitive.add_vertex(new_point, new_uv_point, new_normal)
                new_vertex3 = primitive.add_vertex(new_point, new_uv_point, new_normal)

                primitive.add_triangle(new_vertex1, new_vertex2, new_vertex3)

            for primitive in sub_object.primitives(prim_state_name="Rails"):
                primitive.remove_triangles_connected_to(vertex)
                primitive.remove_triangle(vertex1, vertex2, vertex3)

shapeio.dump(my_shape, "./path/to/output.s")
```

## Running Tests

You can run tests manually or use `tox` to test across multiple Python versions.

### Run Tests Manually
First, install the required dependencies:

```sh
pip install pytest
```

Then, run tests with:

```sh
pytest
```


## Run Tests with `tox`

`tox` allows you to test across multiple Python environments.

### **1. Install `tox`**
```sh
pip install tox
```

### **2. Run Tests**
```sh
tox
```

This will execute tests in all specified Python versions.

### **3. `tox.ini` Configuration**
The `tox.ini` file should be in your project root:

```ini
[tox]
envlist = py36, py37, py38, py39, py310

[testenv]
deps = pytest
commands = pytest
```

Modify `envlist` to match the Python versions you want to support.

## License

This Python module was created by Peter Grønbæk Andersen and is licensed under [GNU GPL v3](/LICENSE).
