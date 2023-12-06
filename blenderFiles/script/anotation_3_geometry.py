import bpy
import sys
import csv
import math
import os

# clean

def deactivate_select():
    bpy.context.view_layer.objects.active = None
    for obj in bpy.context.scene.objects:
        obj.select_set(False)
    return


def deleteAllObjects():
    """
    Deletes all objects in the current scene
    """
    deleteListObjects = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'HAIR', 'POINTCLOUD', 'VOLUME', 'GPENCIL',
                     'ARMATURE', 'LATTICE', 'EMPTY', 'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER']

    # Select all objects in the scene to be deleted:

    for o in bpy.context.scene.objects:
        for i in deleteListObjects:
            if o.type == i:
                o.select_set(False)
            else:
                o.select_set(True)
    # Deletes all selected objects in the scene:

    bpy.ops.object.delete() 

def addPointLight(lightName="light"):
    # Add light

    light_data = bpy.data.lights.new(name=lightName, type="POINT")
    light_data.energy = 2000
    light_object = bpy.data.objects.new('Light', light_data)
    bpy.context.scene.collection.objects.link(light_object)

    light_object.location = (1, 0, 4)

def activator(obj_name_to_activate):
    for obj in bpy.context.scene.objects:
        if obj.name == obj_name_to_activate:
            bpy.context.view_layer.objects.active = obj
    return

def material1(tex_path):
    
    mat = bpy.data.materials.new(name='mat1')
    mat.use_nodes = True
    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()
    bpy.context.active_object.data.materials.clear()
    bpy.context.active_object.data.materials.append(mat)
    
    
    mat_nodes = mat.node_tree.nodes
    mat_link = mat.node_tree.links

    material_output = mat_nodes.new('ShaderNodeOutputMaterial')
    bsdf1_output = mat_nodes.new("ShaderNodeBsdfPrincipled")

    ImgTex_node = mat_nodes.new('ShaderNodeTexImage')
    ImgTex_node.image = bpy.data.images.load(tex_path)
    
    mat_link.new(ImgTex_node.outputs[0], bsdf1_output.inputs[0])
    mat_link.new(bsdf1_output.outputs[0], material_output.inputs[0])
    return mat

def some_other_function(dummy):
    print("some other function")
    bpy.ops.wm.quit_blender()

if __name__=="__main__":
    argv = sys.argv
    argv = argv[argv.index("--")+1:]

    csv_file = argv[0]
    tex_path = argv[1]
    tex_path2 = argv[2]
    save_path = argv[3]
    obj_path_main = argv[4]
    camera_location = []
    object_location = []
    object_rotation = []
    # csv_file = "/home/aru/phd/objective2/blender/blendFile/renderedImage/renderData/img1.csv"
    file_name = os.path.basename(csv_file).split(sep=".")[0]
    with open(csv_file, "r") as f:
        csv_reader = csv.DictReader(f, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print(row)
            print(type(row))
            camera_location.append(float(row["camera_x"]))
            camera_location.append(float(row["camera_y"]))
            camera_location.append(float(row["camera_z"]))
            object_location.append(float(row["x_location"]))
            object_location.append(float(row["y_location"]))
            object_rotation.append(float(row["x_rotaiton"]))
            object_rotation.append(float(row["y_ratation"]))
            object_rotation.append(float(row["z_rotation"]))
            obj_file = row["obj_file"]
            tex_file = row["tex_file"]
            tex_file2 = row["tex_file2"]
            line_count += 1

    deleteAllObjects()
    print(camera_location)
    print(object_location)
    print(object_rotation)
    print(obj_file)
    print(tex_file)
    tex_file_name = os.path.basename(tex_file)
    tex_file2_name = os.path.basename(tex_file2)
    obj_file_name = os.path.basename(obj_file)
    anotation_tex_file = tex_path+tex_file_name
    anotation_tex_file2 = tex_path2+tex_file2_name
    obj_path = obj_path_main + "1/" + obj_file_name
    if not os.path.exists(obj_path):
        print("not in {}".format(obj_path))
        obj_path = obj_path_main + "2/" + obj_file_name
        if not os.path.exists(obj_path):
            print("not in {}".format(obj_path))
            obj_path = obj_path_main + "3/" + obj_file_name
            if not os.path.exists(obj_path):
                print("not in {}".format(obj_path))
                obj_path = obj_path_main + "5/" + obj_file_name
    # Add camera
    camera_data = bpy.data.cameras.new(name='Camera')
    camera_object = bpy.data.objects.new('Camera', camera_data)
    bpy.context.scene.collection.objects.link(camera_object)
    #bpy.data.objects["Camera"].rotation_euler = (0, 0, 0)
    bpy.data.objects["Camera"].location = tuple(camera_location)

    addPointLight()


    # Add object (use for loob to add all model subsiquently)

    imported_object = bpy.ops.import_scene.obj(filepath=obj_path)
    obj_object = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = obj_object
    object_name = obj_object.name
    activator(object_name)
    print('Imported name: ', obj_object.name)
    bpy.ops.object.shade_smooth()


    bpy.data.objects[object_name].scale = (0.001, 0.001, 0.001)
    bpy.data.objects[object_name].rotation_euler = (math.radians(object_rotation[0]), math.radians(object_rotation[1]), math.radians(object_rotation[2]))
    bpy.data.objects[object_name].location = (object_location[0], object_location[1], 0)

    # Texture to use (use glob and for loob to generate image for each crack texture)
    mat = material1(anotation_tex_file)

    deactivate_select()

    # Add second geometry

    parent_path = os.path.dirname(obj_path)
    base_name = os.path.basename(obj_file)
    obj2_file = parent_path+"/separate1/"+base_name
    imported_object = bpy.ops.import_scene.obj(filepath=obj2_file)
    obj_object = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = obj_object
    object_name = obj_object.name
    activator(object_name)
    print('Imported name: ', obj_object.name)
    bpy.ops.object.shade_smooth()

    bpy.data.objects[object_name].scale = (0.001, 0.001, 0.001)
    bpy.data.objects[object_name].rotation_euler = (math.radians(object_rotation[0]), math.radians(object_rotation[1]), math.radians(object_rotation[2]))
    bpy.data.objects[object_name].location = (object_location[0], object_location[1], 0)

    bpy.context.active_object.data.materials.clear()
    bpy.context.active_object.data.materials.append(mat)

    deactivate_select()
    # Add Third geometry

    obj3_file = parent_path+"/separate2/"+base_name
    imported_object = bpy.ops.import_scene.obj(filepath=obj3_file)
    obj_object = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = obj_object
    object_name = obj_object.name
    activator(object_name)
    print('Imported name: ', obj_object.name)
    bpy.ops.object.shade_smooth()

    bpy.data.objects[object_name].scale = (0.001, 0.001, 0.001)
    bpy.data.objects[object_name].rotation_euler = (math.radians(object_rotation[0]), math.radians(object_rotation[1]), math.radians(object_rotation[2]))
    bpy.data.objects[object_name].location = (object_location[0], object_location[1], 0)

    bpy.context.active_object.data.materials.clear()
    mat2 = material1(anotation_tex_file2)
        ## Rending
    save_file = save_path + file_name
    bpy.context.scene.render.filepath = save_file
    bpy.data.scenes["Scene"].render.image_settings.file_format = "PNG"
    bpy.data.scenes["Scene"].render.resolution_y = 1024
    bpy.data.scenes["Scene"].render.resolution_x = 1024

    bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)
    bpy.app.handlers.render_complete.append(some_other_function)