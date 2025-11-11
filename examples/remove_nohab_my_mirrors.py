import os
import pyffeditc
import shapeio
from shapeedit import ShapeEditor

if __name__ == "__main__":
    ffeditc_path = "./ffeditc_unicode.exe"
    load_path = "/media/peter/T7 Shield/TRAINS/TRAINSET/My Nohab"
    processed_path = "/media/peter/T7 Shield/TRAINS/TRAINSET/My Nohab"
    locomotive_shape = "DSB_My1135.s"
    new_locomotive_shape = "DSB_My1135_no_mirrors.s"
    
    os.makedirs(processed_path, exist_ok=True)

    shape_path = f"{load_path}/{locomotive_shape}"
    new_shape_path = f"{processed_path}/{new_locomotive_shape}"

    shapeio.copy(shape_path, new_shape_path)

    pyffeditc.decompress(ffeditc_path, new_shape_path)
    shape = shapeio.load(new_shape_path)

    shape_editor = ShapeEditor(shape)

    for lod_control in shape_editor.lod_controls():
        for lod_dlevel in lod_control.distance_levels():
            for sub_object in lod_dlevel.sub_objects():
                for primitive in sub_object.primitives():
                    for vertex in primitive.vertices():
                        # Define the Z ranges for the mirrors
                        in_positive_z = 6.67818 <= vertex.point.z <= 7.05782
                        in_negative_z = -7.05782 <= vertex.point.z <= -6.67818

                        # Define four separate XY boxes, one for each mirror
                        in_box_1 = (1.43495 <= vertex.point.x <= 1.68895) and (1.77872 <= vertex.point.y <= 2.32183)
                        in_box_2 = (-1.68895 <= vertex.point.x <= -1.43495) and (1.77872 <= vertex.point.y <= 2.32183)
                        in_box_3 = (1.43495 <= vertex.point.x <= 1.68895) and (-2.32183 <= vertex.point.y <= -1.77872)
                        in_box_4 = (-1.68895 <= vertex.point.x <= -1.43495) and (-2.32183 <= vertex.point.y <= -1.77872)

                        is_mirror = (in_positive_z or in_negative_z) and (in_box_1 or in_box_2 or in_box_3 or in_box_4)

                        if is_mirror:
                            primitive.remove_triangles_connected_to(vertex)

    shapeio.dump(shape, new_shape_path)

