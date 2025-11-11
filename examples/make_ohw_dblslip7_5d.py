import os
import pyffeditc
import shapeio
from shapeedit import ShapeEditor
from shapeedit.math import coordinates

if __name__ == "__main__":
    ffeditc_path = "./ffeditc_unicode.exe"
    load_path = "./examples/data"
    processed_path = "./examples/data/processed/OhwDblSlip7_5d"
    cwire_shape = "DB22f_A1tDblSlip7_5d.s"
    match_files = ["DB2_A1tDblSlip7_5d.s", "DB3_A1tDblSlip7_5d.s", "DB2_A1tDKW7_5d.s", "DB3_A1tDKW7_5d.s"]
    ignore_files = ["*.sd"]
    
    os.makedirs(processed_path, exist_ok=True)

    cwire_shape_path = f"{load_path}/{cwire_shape}"

    pyffeditc.decompress(ffeditc_path, cwire_shape_path)
    cwire_shape = shapeio.load(cwire_shape_path)
    
    cwire_shape_editor = ShapeEditor(cwire_shape)
    cwire_sub_object = cwire_shape_editor.lod_control(0).distance_level(200).sub_object(3)
    cwire_primitives = cwire_sub_object.primitives(prim_state_name="mt_cwire")

    shape_names = shapeio.find_directory_files(load_path, match_files, ignore_files)

    for idx, sfile_name in enumerate(shape_names):
        print(f"Shape {idx + 1} of {len(shape_names)}...")
        new_sfile_name = sfile_name.replace("DB2_", "DB2f_")
        new_sfile_name = new_sfile_name.replace("DB3_", "DB3f_")

        shape_path = f"{load_path}/{sfile_name}"
        new_shape_path = f"{processed_path}/{new_sfile_name}"

        shapeio.copy(shape_path, new_shape_path)

        pyffeditc.decompress(ffeditc_path, new_shape_path)
        trackshape = shapeio.load(new_shape_path)

        shape_editor = ShapeEditor(trackshape)
        sub_object = shape_editor.lod_control(0).distance_level(500).sub_object(0)

        primitive = sub_object.primitives(prim_state_name="Material_#1")[0]
        to_matrix = primitive.matrix
        
        for cwire_primitive in cwire_primitives:
            cwire_vertices = cwire_primitive.vertices()
            cwire_triangles = cwire_primitive.triangles()
            from_matrix = cwire_primitive.matrix

            # Insert vertices from 'cwire_primitive' into 'primitive'.
            new_vertex_lookup = {} # Key is vertex index within cwire_sub_object, value is new_vertex.

            for idx, cwire_vertex in enumerate(cwire_vertices):
                print(f"\tInserting vertex {idx + 1} of {len(cwire_vertices)}", end='\r')
                new_vertex = primitive.add_vertex(cwire_vertex.point, cwire_vertex.uv_point, cwire_vertex.normal)

                new_vertex.point = coordinates.remap_point(new_vertex.point, from_matrix, to_matrix)
                new_vertex.normal = coordinates.remap_normal(new_vertex.normal, from_matrix, to_matrix)

                if cwire_vertex.index not in new_vertex_lookup:
                    new_vertex_lookup[cwire_vertex.index] = new_vertex
            
            print("")

            # Insert triangles from 'cwire_primitive' into 'primitive'.
            for idx, cwire_triangle in enumerate(cwire_triangles):
                print(f"\tInserting triangle {idx + 1} of {len(cwire_triangles)}", end='\r')
                cwire_triangle_vertices = cwire_triangle.vertices()
                vertex1 = new_vertex_lookup[cwire_triangle_vertices[0].index]
                vertex2 = new_vertex_lookup[cwire_triangle_vertices[1].index]
                vertex3 = new_vertex_lookup[cwire_triangle_vertices[2].index]
                new_triangle = primitive.insert_triangle(vertex1, vertex2, vertex3)

                new_triangle.face_normal = coordinates.remap_normal(new_triangle.face_normal, from_matrix, to_matrix)
            
            print("")
            
        shapeio.dump(trackshape, new_shape_path)
        #pyffeditc.compress(ffeditc_path, new_shape_path)

        # Process .sd file
        sdfile_name = sfile_name.replace(".s", ".sd")
        new_sdfile_name = new_sfile_name.replace(".s", ".sd")

        sdfile_path = f"{load_path}/{sdfile_name}"
        new_sdfile_path = f"{processed_path}/{new_sdfile_name}"

        shapeio.copy(sdfile_path, new_sdfile_path)
        shapeio.replace_ignorecase(new_sdfile_path, sfile_name, new_sfile_name)
