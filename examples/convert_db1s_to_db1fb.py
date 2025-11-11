import os
import re
import pyffeditc
import shapeio
from shapeio.shape import Point, UVPoint, Vector
from shapeedit import ShapeEditor

if __name__ == "__main__":
    ffeditc_path = "./ffeditc_unicode.exe"
    load_path = "./examples/data"
    processed_path = "./examples/data/processed/DB1fb"
    match_files = ["DB1s_*.s"]
    ignore_files = ["*Tun*", "*Pnt*", "*Frog*"]
    
    os.makedirs(processed_path, exist_ok=True)

    shape_names = shapeio.find_directory_files(load_path, match_files, ignore_files)

    for idx, sfile_name in enumerate(shape_names):
        print(f"Shape {idx + 1} of {len(shape_names)}...")
        
        new_sfile_name = sfile_name.replace("DB1s", "DB1fb")

        # Convert .s file
        shape_path = f"{load_path}/{sfile_name}"
        new_shape_path = f"{processed_path}/{new_sfile_name}"

        shapeio.copy(shape_path, new_shape_path)

        pyffeditc.decompress(ffeditc_path, new_shape_path)
        trackshape = shapeio.load(new_shape_path)

        for idx, image in enumerate(trackshape.images):
            image = re.sub(r"DB_TrackSfs1.ace", "DB_Track1.ace", image, flags=re.IGNORECASE)
            image = re.sub(r"DB_TrackSfs1s.ace", "DB_Track1s.ace", image, flags=re.IGNORECASE)
            image = re.sub(r"DB_TrackSfs1w.ace", "DB_Track1w.ace", image, flags=re.IGNORECASE)
            image = re.sub(r"DB_TrackSfs1sw.ace", "DB_Track1sw.ace", image, flags=re.IGNORECASE)
            trackshape.images[idx] = image

        trackshape_editor = ShapeEditor(trackshape)
        lod_control = trackshape_editor.lod_control(0)

        for lod_dlevel in lod_control.distance_levels():
            for sub_object in lod_dlevel.sub_objects():
                vertices_in_subobject = sub_object.vertices()
                for vertex in vertices_in_subobject:
                    if vertex.point.y == 0.133:
                        vertex.point.y = 0.0833
                    elif vertex.point.y == 0.145:
                        vertex.point.y = 0.0945
        
        shapeio.dump(trackshape, new_shape_path)
        #pyffeditc.compress(ffeditc_path, new_shape_path)

        # Process .sd file
        sdfile_name = sfile_name.replace(".s", ".sd")
        new_sdfile_name = new_sfile_name.replace(".s", ".sd")

        sdfile_path = f"{load_path}/{sdfile_name}"
        new_sdfile_path = f"{processed_path}/{new_sdfile_name}"

        shapeio.copy(sdfile_path, new_sdfile_path)
        shapeio.replace_ignorecase(new_sdfile_path, sfile_name, new_sfile_name)