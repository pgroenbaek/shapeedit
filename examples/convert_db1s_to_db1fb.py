import os
import pytkutils
import shapeio
from shapeedit import ShapeEditor

if __name__ == "__main__":
    tkutils_dll_path = "./TK.MSTS.Tokens.dll"
    shape_load_path = "./examples/data"
    shape_processed_path = "./examples/data/processed/DB1fb"
    match_shapes = ["DB1s_*.s"]
    ignore_shapes = ["*Tun*", "*Pnt*", "*Frog*"]
    
    os.makedirs(shape_processed_path, exist_ok=True)

    shape_names = shapeio.find_directory_files(shape_load_path, match_shapes, ignore_shapes)

    for idx, sfile_name in enumerate(shape_names):
        print(f"Shape {idx + 1} of {len(shape_names)}...")
        
        # Convert .s file
        new_sfile_name = sfile_name.replace("DB1s_", "DB1fb_")

        shape_path = f"{shape_load_path}/{sfile_name}"
        new_shape_path = f"{shape_processed_path}/{new_sfile_name}"

        shapeio.copy(shape_path, new_shape_path)

        pytkutils.decompress(tkutils_dll_path, new_shape_path)

        shapeio.replace_ignorecase(new_shape_path, "DB_TrackSfs1.ace", "DB_Track1.ace")
        shapeio.replace_ignorecase(new_shape_path, "DB_TrackSfs1s.ace", "DB_Track1s.ace")
        shapeio.replace_ignorecase(new_shape_path, "DB_TrackSfs1w.ace", "DB_Track1w.ace")
        shapeio.replace_ignorecase(new_shape_path, "DB_TrackSfs1sw.ace", "DB_Track1sw.ace")

        trackshape = shapeio.load(new_shape_path)

        trackshape_editor = ShapeEditor(trackshape)
        distance_level = trackshape_editor.lod_control(0).distance_level(500)
,
        for sub_object in distance_level.sub_objects():
            for vertex in sub_object.vertices():
                if vertex.point.y == 0.133:
                    vertex.point.y = 0.0833
                elif vertex.point.y == 0.145:
                    vertex.point.y = 0.0945

        shapeio.dump(trackshape, new_shape_path)
        pytkutils.compress(tkutils_dll_path, new_shape_path)

        # Convert .sd file
        sdfile_name = sfile_name.replace(".s", ".sd")
        new_sdfile_name = new_sfile_name.replace(".s", ".sd")

        sdfile_path = f"{shape_load_path}/{sdfile_name}"
        new_sdfile_path = f"{shape_processed_path}/{new_sdfile_name}"

        shapeio.copy(sdfile_path, new_sdfile_path)
        shapeio.replace_ignorecase(new_sdfile_path, sfile_name, new_sfile_name)