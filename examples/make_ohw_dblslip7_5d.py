import os
import shapeio
import pytkutils
from shapeedit import ShapeEditor
from shapeedit.math import coordinates

if __name__ == "__main__":
    tkutils_dll_path = "./TK.MSTS.Tokens.dll"
    shape_load_path = "./examples/data"
    shape_processed_path = "./examples/data/processed/OhwDblSlip7_5d"
    cwire_shape = "DB2f_A1tDblSlip7_5d_original.s"
    match_files = ["DB2_A1tDblSlip7_5d.s", "DB3_A1tDblSlip7_5d.s", "DB2_A1tDKW7_5d.s", "DB3_A1tDKW7_5d.s"]
    ignore_files = []
    
    os.makedirs(shape_processed_path, exist_ok=True)

    cwire_shape_path = f"{shape_load_path}/{cwire_shape}"

    pytkutils.decompress(tkutils_dll_path, cwire_shape_path)
    cwire_shape = shapeio.load(cwire_shape_path)

    cwire_editor = ShapeEditor(cwire_shape)
    cwire_subobject = cwire_editor.lod_control(0).distance_level(200).sub_object(3)
    cwire_primitives = cwire_subobject.primitives(prim_state_name="mt_cwire")

    shape_names = shapeio.find_directory_files(shape_load_path, match_files, ignore_files)

    for idx, sfile_name in enumerate(shape_names):
        print(f"Shape {idx + 1} of {len(shape_names)}...")
        new_sfile_name = sfile_name.replace("DB2_", "DB2f_")
        new_sfile_name = new_sfile_name.replace("DB3_", "DB3f_")

        shape_path = f"{shape_load_path}/{sfile_name}"
        new_shape_path = f"{shape_processed_path}/{new_sfile_name}"

        shapeio.copy(shape_path, new_shape_path)

        pytkutils.decompress(tkutils_dll_path, new_shape_path)
        trackshape = shapeio.load(new_shape_path)

        trackshape_editor = ShapeEditor(trackshape)
        trackshape_subobject = trackshape_editor.lod_control(0).distance_level(500).sub_object(0)
        trackshape_primitive = trackshape_subobject.primitives(prim_state_name="Material_#1")[0]

        to_matrix = trackshape_primitive.matrix

        for cwire_primitive in cwire_primitives:
            cwire_vertices = cwire_primitive.vertices()
            cwire_triangles = cwire_primitive.triangles()
            from_matrix = cwire_primitive.matrix

            print(f"Processing '{from_matrix.name}' vertices")

            new_vertex_lookup = {} # Key is vertex_idx of mt_cwire, value is new_vertex.

            # Re-map points and normals from the matrices in Norbert Rieger's
            # shape to fit the Material_#1 matrix of Laci1959's shape.
            for cwire_vertex in cwire_vertices:
                remapped_point = coordinates.remap_point(cwire_vertex.point, from_matrix, to_matrix)
                remapped_normal = coordinates.remap_normal(cwire_vertex.normal, from_matrix, to_matrix)

                print(f"\tAdding vertex {idx + 1} of {len(cwire_vertices)}", end='\r')
                new_vertex = trackshape_primitive.add_vertex(remapped_point, cwire_vertex.uv_point, remapped_normal)
                new_vertex_lookup[cwire_vertex.index] = new_vertex
            
            print("")
            
            for cwire_triangle in cwire_triangles:
                print(f"\tInserting triangle {idx + 1} of {len(cwire_triangles)}", end='\r')
                cwire_triangle_vertices = cwire_triangle.vertices()
                vertex1 = new_vertex_lookup[cwire_triangle_vertices[0].index]
                vertex2 = new_vertex_lookup[cwire_triangle_vertices[1].index]
                vertex3 = new_vertex_lookup[cwire_triangle_vertices[2].index]
                new_triangle = trackshape_primitive.insert_triangle(vertex1, vertex2, vertex3)

                remapped_facenormal = coordinates.remap_normal(cwire_triangle.face_normal, from_matrix, to_matrix)
                new_triangle.face_normal = remapped_facenormal
            
            print("")
            
        shapeio.dump(trackshape, new_shape_path)
        pytkutils.compress(tkutils_dll_path, new_shape_path)

        sdfile_name = sfile_name.replace(".s", ".sd")
        new_sdfile_name = new_sfile_name.replace(".s", ".sd")

        sdfile_path = f"{shape_load_path}/{sdfile_name}"
        new_sdfile_path = f"{shape_processed_path}/{new_sdfile_name}"

        shapeio.copy(sdfile_path, new_sdfile_path)
        shapeio.replace_ignorecase(new_sdfile_path, sfile_name, new_sfile_name)
