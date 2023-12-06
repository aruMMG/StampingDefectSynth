import bpy
import os
import random
import math
import argparse
import sys
from pathlib import Path
import csv
import numpy as np
# import pdb

# clean

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



def activator(obj_name_to_activate):
    for obj in bpy.context.scene.objects:
        if obj.name == obj_name_to_activate:
            bpy.context.view_layer.objects.active = obj
    return

def deactivate_select():
    bpy.context.view_layer.objects.active = None
    for obj in bpy.context.scene.objects:
        obj.select_set(False)
    return

def newMaterial(id):

    mat = bpy.data.materials.get(id)

    if mat is None:
        mat = bpy.data.materials.new(name=id)

    mat.use_nodes = True

    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()

    return mat


def addAreaLight(lightName):
    # Add light

    light_data = bpy.data.lights.new(name=lightName, type="AREA")
    energy = np.clip(np.random.normal(loc=850000, scale=100000), a_min=600000, a_max=1100000)
#    energy = int(random.uniform(1000,2000))
    light_data.energy = energy
    light_data.spread = math.radians(90)
    b = random.uniform(0.65, 0.9)
    g = random.uniform(0.9, 0.95)
    light_data.color = (1, g, b)
    light_object = bpy.data.objects.new('Light', light_data)
    bpy.context.scene.collection.objects.link(light_object)

    x_location = 3.5
    y_location = -1
    z_location = 4
    light_object.location = (x_location, y_location, z_location)


def addPointLight(lightName):
    # Add light

    light_data = bpy.data.lights.new(name=lightName, type="POINT")
    energy = 400000 # int(random.uniform(200000,400000))
#    energy = int(random.uniform(1000,2000))
    light_data.energy = energy
    light_object = bpy.data.objects.new('Light', light_data)
    bpy.context.scene.collection.objects.link(light_object)

        # Random light location
        
    x_location = 2
    y_location = -1
    z_location = 4
    #     x_location = random.uniform(-3,3)
    # y_location = random.uniform(-3,3)
    # z_location = random.uniform(3,6)
    #bpy.data.objects["Camera"].rotation_euler = (0, 0, 0)
    light_object.location = (x_location, y_location, z_location)

def randomiseMapping(Mapping_node):
    if random.randint(1,2)==1:
        Mapping_node.inputs[1].default_value = (random.uniform(-1,1), random.uniform(-1, 1), random.uniform(-1, 1))
#        Mapping_node.inputs[2].default_value = (math.radians(random.uniform(0,360)), math.radians(random.uniform(0,360)), math.radians(random.uniform(0,360)))
        Mapping_node.inputs[3].default_value = (random.uniform(0.01, 0.0004), random.uniform(0.01, 0.0004), random.uniform(0.01, 0.0004))
    else:
        scale_value = random.uniform(0.01, 0.0004)
        rotation_value = math.radians(random.uniform(0, 360))
        location_value = random.uniform(-1, 1)
        Mapping_node.inputs[1].default_value = (location_value, location_value, location_value)
#        Mapping_node.inputs[2].default_value = (rotation_value, rotation_value, rotation_value)
        Mapping_node.inputs[3].default_value = (scale_value, scale_value, scale_value)

def scratch(mat_nodes, TexCoord_node, mat_link, bsdf2_output):
    pass
def material1(tex_path):
    
    mat = bpy.data.materials.new(name='mat1')
    mat.use_nodes = True
    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()
    mat_name = mat.name
    bpy.context.active_object.data.materials.clear()
    bpy.context.active_object.data.materials.append(mat)
#    obj = bpy.context.collection.objects[obj_name]
#    obj.data.materials.append(mat)
    
    
    mat_nodes = mat.node_tree.nodes
    mat_link = mat.node_tree.links

    material_output = mat_nodes.new('ShaderNodeOutputMaterial')
    bsdf1_output = mat_nodes.new("ShaderNodeBsdfPrincipled")
    bsdf1_output.inputs[6].default_value = 1
    bsdf2_output = mat_nodes.new("ShaderNodeBsdfPrincipled")
    bsdf2_output.inputs[6].default_value = 1
    bsdf2_output.inputs[9].default_value = 0.26
#    bsdf3_output = mat_nodes.get("Principled BSDF")
    
    material_output.location = (1600,-400)
    bsdf1_output.location = (-600,0)
    bsdf2_output.location = (-600,-800)
#    bsdf3_output.location = (-600,1200)
    
    TexCoord_node = mat_nodes.new('ShaderNodeTexCoord')
    TexCoord_node.location = (-3200, -400)

    Mapping1_node = mat_nodes.new('ShaderNodeMapping')
    Mapping1_node.location = (-1400, -400)
#    randomiseMapping(Mapping1_node)
    Mapping1_node.inputs[1].default_value = (random.uniform(-0.4,-0.7), random.uniform(-0.4, -0.7), random.uniform(-0.4, -0.7))
    Mapping1_node.inputs[3].default_value = (random.uniform(0.01, 0.006), random.uniform(0.006, 0.002), random.uniform(0.01, 0.001))
    Mapping1_node.inputs[2].default_value = (0, 0, math.radians(random.uniform(0,90)))
    #Chocofor1 for metal color
    ImgTex_node = mat_nodes.new('ShaderNodeTexImage')
    ImgTex_node.location = (-1200, -400)
    tex_base = ["tex.jpg", "tex1.jpg"]
    idx = random.randint(0,1) 
    ImgTex_node.image = bpy.data.images.load('/home/aru/run6/40/'+tex_base[idx])
    # ImgTex_node.image = bpy.data.images.load('/home/aru/run6/40/tex.jpg')


    mixRGB1_node = mat_nodes.new("ShaderNodeMixRGB")
    mixRGB1_node.location = (-900, 0)
    mixRGB2_node = mat_nodes.new("ShaderNodeMixRGB")
    mixRGB2_node.location = (-900, -800)
    
    #Color Ramp
    colramp_node = mat_nodes.new("ShaderNodeValToRGB")
    colramp_node.location = (-900, -400)
    colramp_node.color_ramp.interpolation = "B_SPLINE"
    colramp_node.color_ramp.elements[0].position = 0.141
    colramp_node.color_ramp.elements[1].position = 0.77
    colramp_node.color_ramp.elements[0].color = (0.2,0.2,0.2,1)
    colramp_node.color_ramp.elements[1].color = (1,1,1,1)
    
    mat_link.new(TexCoord_node.outputs[3], Mapping1_node.inputs[0])
    mat_link.new(Mapping1_node.outputs[0], ImgTex_node.inputs[0])
    mat_link.new(ImgTex_node.outputs[0], mixRGB1_node.inputs[1])
    mat_link.new(ImgTex_node.outputs[0], mixRGB2_node.inputs[1])
    mat_link.new(ImgTex_node.outputs[0], colramp_node.inputs[0])
    mat_link.new(mixRGB1_node.outputs[0], bsdf1_output.inputs[0])
    mat_link.new(mixRGB2_node.outputs[0], bsdf2_output.inputs[0])
    mat_link.new(colramp_node.outputs[0], bsdf1_output.inputs[9])

    #Chocofor4 to mix shader
    
    MappingMixShader_node = mat_nodes.new('ShaderNodeMapping')
    MappingMixShader_node.location = (-1400, 400)
    randomiseMapping(MappingMixShader_node)
#    MappingMixShader_node.inputs[3].default_value = (0.001, 0.001, 0.001)
#    MappingMixShader_node.inputs[3].default_value = (0.001, 0.001, 0.001)
    
    ImgTexToMixShader_node = mat_nodes.new('ShaderNodeTexImage')
    ImgTexToMixShader_node.location = (-400, 400)
    ImgTexToMixShader_node.image = bpy.data.images.load('/home/aru/run6/40/Chocofur_Metal_Solid_04_diff.jpg')
    
    separateRGB_node = mat_nodes.new("ShaderNodeSeparateRGB")
    separateRGB_node.location = (0,400)
    
    #Color Ramp to mix shader
    colramp1_node = mat_nodes.new("ShaderNodeValToRGB")
    colramp1_node.location = (400, 400)
    colramp1_node.color_ramp.interpolation = "LINEAR"
    colramp1_node.color_ramp.elements[0].position = 0.2
    colramp1_node.color_ramp.elements[1].position = 0.77
    colramp1_node.color_ramp.elements[0].color = (0,0,0,1)
    colramp1_node.color_ramp.elements[1].color = (1,1,1,1)

    mixShader_node = mat_nodes.new("ShaderNodeMixShader")
    mixShader_node.location = (700,0)

    
    mat_link.new(TexCoord_node.outputs[3], MappingMixShader_node.inputs[0])
    mat_link.new(MappingMixShader_node.outputs[0], ImgTexToMixShader_node.inputs[0])
    mat_link.new(ImgTexToMixShader_node.outputs[0], separateRGB_node.inputs[0])
    mat_link.new(separateRGB_node.outputs[0], colramp1_node.inputs[0])
    mat_link.new(colramp1_node.outputs[0], mixShader_node.inputs[0])
    mat_link.new(bsdf1_output.outputs[0], mixShader_node.inputs[1])
    mat_link.new(bsdf2_output.outputs[0], mixShader_node.inputs[2])


    
    # Displacement map
    Mapping2_node = mat_nodes.new('ShaderNodeMapping')
    Mapping2_node.location = (-1400, -1200)    
    
    # crack image texture
    ImgTexCrack_node = mat_nodes.new('ShaderNodeTexImage')
    ImgTexCrack_node.location = (0, -800)
    ImgTexCrack_node.image = bpy.data.images.load(tex_path)
    
    Displacement_node = mat_nodes.new('ShaderNodeDisplacement')
    Displacement_node.location = (400, -1000) 
    
    mat_link.new(TexCoord_node.outputs[2], Mapping2_node.inputs[0])
    mat_link.new(Mapping2_node.outputs[0], ImgTexCrack_node.inputs[0])
    mat_link.new(ImgTexCrack_node.outputs[0], Displacement_node.inputs[0])
    mat_link.new(Displacement_node.outputs[0], material_output.inputs[2])
    
    sc1_color_ramp_node = mat_nodes.new('ShaderNodeValToRGB')
    sc1_color_ramp_node.location = (-2000,-800)
    sc1_color_ramp_node.color_ramp.elements[0].position = 0.674
    sc1_color_ramp_node.color_ramp.elements[1].position = 0.664
    sc2_color_ramp_node = mat_nodes.new('ShaderNodeValToRGB')
    sc2_color_ramp_node.color_ramp.elements[0].position = 0.674
    sc2_color_ramp_node.color_ramp.elements[1].position = 0.664
    sc2_color_ramp_node.location = (-2000,-400)
    sc3_color_ramp_node = mat_nodes.new('ShaderNodeValToRGB')
    sc3_color_ramp_node.location = (-2000,0)
    sc3_color_ramp_node.color_ramp.elements[0].position = 0.464
    sc3_color_ramp_node.color_ramp.elements[1].position = random.uniform(0.468, 0.47)
    sc3_color_ramp_node2 = mat_nodes.new('ShaderNodeValToRGB')
    sc3_color_ramp_node2.location = (-2000,400)
    sc3_color_ramp_node2.color_ramp.elements[1].position = random.uniform(0.002, 0.004)
    sc4_color_ramp_node = mat_nodes.new('ShaderNodeValToRGB')
    sc4_color_ramp_node.location = (-2000,800)
    sc4_color_ramp_node.color_ramp.elements[0].position = 0.464
    sc4_color_ramp_node.color_ramp.elements[1].position = random.uniform(0.468, 0.47)
    sc4_color_ramp_node2 = mat_nodes.new('ShaderNodeValToRGB')
    sc4_color_ramp_node2.location = (-2000,1200)
    sc4_color_ramp_node2.color_ramp.elements[1].position = random.uniform(0.002, 0.004)

    sc1_NoiseTex_node = mat_nodes.new('ShaderNodeTexNoise')
    sc1_NoiseTex_node.location = (-2400,-800)

    sc2_NoiseTex_node = mat_nodes.new('ShaderNodeTexNoise')
    sc2_NoiseTex_node.location = (-2400,-400)

    sc3_vornoiTex_node = mat_nodes.new('ShaderNodeTexVoronoi')
    sc3_vornoiTex_node.location = (-2400, 0)
    sc3_vornoiTex_node.inputs[2].default_value = 0.05

    sc3_vornoiTex_node2 = mat_nodes.new('ShaderNodeTexVoronoi')
    sc3_vornoiTex_node2.location = (-2400, 400)
    sc3_vornoiTex_node2.inputs[2].default_value = 0.05
    sc3_vornoiTex_node2.feature = 'DISTANCE_TO_EDGE'


    sc4_vornoiTex_node = mat_nodes.new('ShaderNodeTexVoronoi')
    sc4_vornoiTex_node.location = (-2400, 800)
    sc4_vornoiTex_node.inputs[2].default_value = 0.05

    sc4_vornoiTex_node2 = mat_nodes.new('ShaderNodeTexVoronoi')
    sc4_vornoiTex_node2.location = (-2400, 1200)
    sc4_vornoiTex_node2.inputs[2].default_value = 0.05
    sc4_vornoiTex_node2.feature = 'DISTANCE_TO_EDGE'

    sc1_Mapping1_node = mat_nodes.new('ShaderNodeMapping')
    sc1_Mapping1_node.location = (-2800, -800)
    sc1_Mapping1_node.inputs[3].default_value = (random.uniform(30,60),1,1)
    sc2_Mapping1_node = mat_nodes.new('ShaderNodeMapping')
    sc2_Mapping1_node.location = (-2800, -400)
    sc2_Mapping1_node.inputs[3].default_value = (1, random.uniform(30,60),1)
    sc3_Mapping1_node = mat_nodes.new('ShaderNodeMapping')
    sc3_Mapping1_node.location = (-2800, 400)
    angles = (math.radians(random.uniform(15,45)), math.radians(random.uniform(15,45)), math.radians(random.uniform(15,45)))
    sc3_Mapping1_node.inputs[2].default_value = (angles)
    sc3_Mapping1_node.inputs[3].default_value = (0.5,0.3,0.7)
    sc4_Mapping1_node = mat_nodes.new('ShaderNodeMapping')
    sc4_Mapping1_node.location = (-2800, 1200)
    sc4_Mapping1_node.inputs[2].default_value = (angles)
    sc4_Mapping1_node.inputs[3].default_value = (0.5,0.5,0.5)
    
    value = random.uniform(10,15)


    sc3_math_node = mat_nodes.new('ShaderNodeMath')
    sc3_math_node.location = (-1600, 400)
    sc3_math_node.use_clamp = True

    sc4_math_node = mat_nodes.new('ShaderNodeMath')
    sc4_math_node.location = (-1600, 800)
    sc4_math_node.use_clamp = True


    sc12_mix_node = mat_nodes.new('ShaderNodeMixRGB')
    sc12_mix_node.location = (-1400, -200)
    sc12_mix_node.blend_type = 'DARKEN'
#    sc12_mix_node.use_clamp = True
    sc12_mix_node.inputs[0].default_value = 0.5

    sc34_mix_node = mat_nodes.new('ShaderNodeMixRGB')
    sc34_mix_node.location = (-1400, 800)
    sc34_mix_node.blend_type = 'DARKEN'
#    sc34_mix_node.use_clamp = True
    sc34_mix_node.inputs[0].default_value = 0.5

    sc_mix_node = mat_nodes.new('ShaderNodeMixRGB')
    sc_mix_node.location = (-1200, 0)
    sc_mix_node.blend_type = 'DARKEN'
#    sc_mix_node.use_clamp = True
    sc_mix_node.inputs[0].default_value = 0.5

    sc_bump_node = mat_nodes.new('ShaderNodeBump')
    sc_bump_node.location = (-800, -1200)
    sc_bump_node.inputs[0].default_value = random.uniform(0.05, 0.15)


    # Linking
    sc1_NoiseTex_node.inputs[2].default_value = value
    sc2_NoiseTex_node.inputs[2].default_value = value

    mat_link.new(TexCoord_node.outputs[0], sc1_Mapping1_node.inputs[0])
    mat_link.new(TexCoord_node.outputs[0], sc2_Mapping1_node.inputs[0])
    mat_link.new(TexCoord_node.outputs[3], sc4_Mapping1_node.inputs[0])
    mat_link.new(TexCoord_node.outputs[3], sc3_Mapping1_node.inputs[0])
    mat_link.new(TexCoord_node.outputs[3], sc3_vornoiTex_node.inputs[0])
    mat_link.new(TexCoord_node.outputs[3], sc3_vornoiTex_node2.inputs[0])

    mat_link.new(sc1_Mapping1_node.outputs[0], sc1_NoiseTex_node.inputs[0])
    mat_link.new(sc2_Mapping1_node.outputs[0], sc2_NoiseTex_node.inputs[0])
    mat_link.new(sc3_Mapping1_node.outputs[0], sc4_vornoiTex_node.inputs[0])
    mat_link.new(sc4_Mapping1_node.outputs[0], sc4_vornoiTex_node2.inputs[0])

    mat_link.new(sc1_NoiseTex_node.outputs[0], sc1_color_ramp_node.inputs[0])
    mat_link.new(sc2_NoiseTex_node.outputs[0], sc2_color_ramp_node.inputs[0])
    mat_link.new(sc3_vornoiTex_node.outputs[0], sc3_color_ramp_node.inputs[0])
    mat_link.new(sc3_vornoiTex_node2.outputs[0], sc3_color_ramp_node2.inputs[0])
    mat_link.new(sc4_vornoiTex_node.outputs[0], sc4_color_ramp_node.inputs[0])
    mat_link.new(sc4_vornoiTex_node2.outputs[0], sc4_color_ramp_node2.inputs[0])

    mat_link.new(sc3_color_ramp_node.outputs[0], sc3_math_node.inputs[1])
    mat_link.new(sc3_color_ramp_node2.outputs[0], sc3_math_node.inputs[0])
    mat_link.new(sc4_color_ramp_node.outputs[0], sc4_math_node.inputs[1])
    mat_link.new(sc4_color_ramp_node2.outputs[0], sc4_math_node.inputs[0])

    mat_link.new(sc1_color_ramp_node.outputs[0], sc12_mix_node.inputs[2])
    mat_link.new(sc2_color_ramp_node.outputs[0], sc12_mix_node.inputs[1])
    mat_link.new(sc3_math_node.outputs[0], sc34_mix_node.inputs[2])
    mat_link.new(sc4_math_node.outputs[0], sc34_mix_node.inputs[1])
    mat_link.new(sc12_mix_node.outputs[0], sc_mix_node.inputs[2])
    mat_link.new(sc34_mix_node.outputs[0], sc_mix_node.inputs[1])

    mat_link.new(sc_mix_node.outputs[0], sc_bump_node.inputs[2])
    mat_link.new(sc_bump_node.outputs[0], bsdf1_output.inputs[22])
    
        #Chocofor1 for imperfection color
    ImgTexImperfection_node = mat_nodes.new('ShaderNodeTexImage')
    ImgTexImperfection_node.location = (-1400, -1400)
    ImgTexImperfection_node.image = bpy.data.images.load('/home/aru/run6/40/imperfection_0002_color_2k.jpg')
    
    MappingImoerfection_node = mat_nodes.new('ShaderNodeMapping')
    MappingImoerfection_node.location = (-1800, -1400)
    scale_value = random.uniform(0.003,0.007)
    MappingImoerfection_node.inputs[3].default_value = (scale_value, scale_value, scale_value)
    
    imperfection_math_node = mat_nodes.new('ShaderNodeMath')
    imperfection_math_node.location = (-1100, -1600)
    imperfection_math_node.operation = "MULTIPLY"
    imperfection_math_node.inputs[1].default_value = random.uniform(15,50)

    imperfection_mixRGB3_node = mat_nodes.new("ShaderNodeMixRGB")
    imperfection_mixRGB3_node.location = (-900, -1400)

    mat_link.new(TexCoord_node.outputs[3], MappingImoerfection_node.inputs[0])
    mat_link.new(ImgTexImperfection_node.outputs[0], imperfection_math_node.inputs[0])
    mat_link.new(imperfection_math_node.outputs[0], imperfection_mixRGB3_node.inputs[2])
    mat_link.new(MappingImoerfection_node.outputs[0], ImgTexImperfection_node.inputs[0])
    mat_link.new(ImgTexImperfection_node.outputs[0], imperfection_mixRGB3_node.inputs[0])
    mat_link.new(ImgTex_node.outputs[0], imperfection_mixRGB3_node.inputs[1])
    
    bsdf3_output = mat_nodes.new("ShaderNodeBsdfPrincipled")
    bsdf3_output.inputs[6].default_value = 1
    bsdf3_output.inputs[9].default_value = 0.26
    bsdf3_output.location = (-600,-1600)

    mat_link.new(imperfection_mixRGB3_node.outputs[0], bsdf3_output.inputs[0])
    
    mixShader2_node = mat_nodes.new("ShaderNodeMixShader")
    mixShader2_node.location = (1000,400)

    mat_link.new(mixShader_node.outputs[0], mixShader2_node.inputs[1])
    mat_link.new(bsdf3_output.outputs[0], mixShader2_node.inputs[2])
    mat_link.new(mixShader2_node.outputs[0], material_output.inputs[0])
    return mat

def segmentMaterial(obj_name, tex_path, mats_name):
    mat1 = bpy.data.materials.new(name='simanticMat')
    mat1.use_nodes = True
    if mat1.node_tree:
        mat1.node_tree.links.clear()
        mat1.node_tree.nodes.clear()
    mats_name.append(mat1.name)
    #    obj = bpy.context.collection.objects[obj_name]
    #    obj.data.materials.append(mat)


    mat_nodes = mat1.node_tree.nodes
    mat_link = mat1.node_tree.links

    material_output = mat_nodes.new('ShaderNodeOutputMaterial')
    bsdf1_output = mat_nodes.new("ShaderNodeBsdfPrincipled")    

    ImgTex_node = mat_nodes.new('ShaderNodeTexImage')
    # ImgTex_node.image = bpy.data.images.load('/home/aru/run5/120/texture/1/DisplacementMap38.png')

    mat_link.new(ImgTex_node.outputs[0],bsdf1_output.inputs[0])
    mat_link.new(bsdf1_output.outputs[0], material_output.inputs[0])
    
def backgroundmat():
    mat = bpy.data.materials.new(name='Backgroundmat')
    mat.use_nodes = True
    bpy.context.active_object.data.materials.append(mat)

    mat_nodes = mat.node_tree.nodes
    mat_link = mat.node_tree.links

    material_output = mat_nodes.get('Material Output')
    bsdf_output = mat_nodes.get("Principled BSDF")
    material_output.location = (-200,0)
    bsdf_output.location = (-600,0)

        # get texture reference
    ImgTex_node = mat_nodes.new('ShaderNodeTexImage')
    ImgTex_node.location = (-1200, -400)
    backgrounds = ["background.JPG", "background1.JPG", "background2.JPG", "background3.JPG"]
    idx = random.randint(0,3) 
    ImgTex_node.image = bpy.data.images.load('/home/aru/run6/40/'+backgrounds[idx])

    mix_node = mat_nodes.new("ShaderNodeMixRGB")
    mix_node.location = (-800, -400)
    mix_node.inputs[0].default_value = 0.95
    mix_node.inputs[2].default_value = (0,0,0, 1)

    bsdf_output.inputs[9].default_value = 0.95

    mat_link.new(ImgTex_node.outputs[0], mix_node.inputs[1])
    mat_link.new(mix_node.outputs[0], bsdf_output.inputs[0])
    mat_link.new(bsdf_output.outputs[0], material_output.inputs[0])
    
    return mat

def addBackgroundObj():
    bpy.ops.mesh.primitive_plane_add()
    bpy.data.objects["Plane"].location = (0,0,-0.05)
    bpy.data.objects["Plane"].dimensions = (0.7,0.4,0)
def addBackground():
        # add background
    bpy.ops.mesh.primitive_plane_add()
    bpy.data.objects["Plane"].location = (0,0,-0.05)
    bpy.data.objects["Plane"].dimensions = (0.7,0.4,0)
        # Create material and assign


    mat = bpy.data.materials.new(name='Backgroundmat')
    mat.use_nodes = True
    bpy.context.active_object.data.materials.append(mat)

    mat_nodes = mat.node_tree.nodes
    mat_link = mat.node_tree.links

    material_output = mat_nodes.get('Material Output')
    bsdf_output = mat_nodes.get("Principled BSDF")
    material_output.location = (-200,0)
    bsdf_output.location = (-600,0)

        # get texture reference
    ImgTex_node = mat_nodes.new('ShaderNodeTexImage')
    ImgTex_node.location = (-1200, -400)
    backgrounds = ["background.JPG", "background1.JPG", "background2.JPG", "background3.JPG"]
    idx = random.randint(0,3) 
    ImgTex_node.image = bpy.data.images.load('/home/aru/run6/40/'+backgrounds[idx])

    mix_node = mat_nodes.new("ShaderNodeMixRGB")
    mix_node.location = (-800, -400)
    mix_node.inputs[0].default_value = 0.95
    mix_node.inputs[2].default_value = (0,0,0, 1)

    bsdf_output.inputs[9].default_value = 0.95

    mat_link.new(ImgTex_node.outputs[0], mix_node.inputs[1])
    mat_link.new(mix_node.outputs[0], bsdf_output.inputs[0])
    mat_link.new(bsdf_output.outputs[0], material_output.inputs[0])

    deactivate_select()            

def addBox(mat):
        # add background
    bpy.ops.mesh.primitive_plane_add()
    bpy.data.objects["Plane.001"].location = (4,0,2.97)
    bpy.data.objects["Plane.001"].dimensions = (4,6.06,0)
    bpy.data.objects["Plane.001"].rotation_euler = (math.radians(90),0,math.radians(90))
    
    bpy.context.active_object.data.materials.clear()
    bpy.context.active_object.data.materials.append(mat)

    deactivate_select()
    
    bpy.ops.mesh.primitive_plane_add()
    bpy.data.objects["Plane.002"].dimensions = (8,6.06,0)
    bpy.data.objects["Plane.002"].location = (0,-2,2.97)
    bpy.data.objects["Plane.002"].rotation_euler = (math.radians(90),0,0)
    
    bpy.context.active_object.data.materials.clear()
    bpy.context.active_object.data.materials.append(mat)

    deactivate_select()
    
    bpy.ops.mesh.primitive_plane_add()
    bpy.data.objects["Plane.003"].location = (-4,0,2.97)
    bpy.data.objects["Plane.003"].dimensions = (4,6.06,0)
    bpy.data.objects["Plane.003"].rotation_euler = (math.radians(90),0,math.radians(90))
    
    bpy.context.active_object.data.materials.clear()
    bpy.context.active_object.data.materials.append(mat)

    deactivate_select()

    bpy.ops.mesh.primitive_plane_add()
    bpy.data.objects["Plane.004"].location = (0,2,2.97)
    bpy.data.objects["Plane.004"].dimensions = (8,6.06,0)
    bpy.data.objects["Plane.004"].rotation_euler = (math.radians(90),0,0)
    
    bpy.context.active_object.data.materials.clear()
    bpy.context.active_object.data.materials.append(mat)

    deactivate_select()

    bpy.ops.mesh.primitive_plane_add()
    bpy.data.objects["Plane.005"].location = (0,0,6)
    bpy.data.objects["Plane.005"].dimensions = (8,4,0)
    
    bpy.context.active_object.data.materials.clear()
    bpy.context.active_object.data.materials.append(mat)

    deactivate_select()

    bpy.ops.mesh.primitive_plane_add()
    bpy.data.objects["Plane.006"].location = (0,0,-0.06)
    bpy.data.objects["Plane.006"].dimensions = (8,4,0)
    
    bpy.context.active_object.data.materials.clear()
    bpy.context.active_object.data.materials.append(mat)

    deactivate_select()          

def some_other_function(dummy):
    print("some other function")
    bpy.ops.wm.quit_blender()

class ArgumentParserForBlender(argparse.ArgumentParser):
    """
    This class is identical to its superclass, except for the parse_args
    method (see docstring). It resolves the ambiguity generated when calling
    Blender from the CLI with a python script, and both Blender and the script
    have arguments. E.g., the following call will make Blender crash because
    it will try to process the script's -a and -b flags:
    >>> blender --python my_script.py -a 1 -b 2

    To bypass this issue this class uses the fact that Blender will ignore all
    arguments given after a double-dash ('--'). The approach is that all
    arguments before '--' go to Blender, arguments after go to the script.
    The following calls work fine:
    >>> blender --python my_script.py -- -a 1 -b 2
    >>> blender --python my_script.py --
    """

    def _get_argv_after_doubledash(self):
        """
        Given the sys.argv as a list of strings, this method returns the
        sublist right after the '--' element (if present, otherwise returns
        an empty list).
        """
        try:
            idx = sys.argv.index("--")
            return sys.argv[idx+1:] # the list after '--'
        except ValueError as e: # '--' not in the list:
            return []

    # overrides superclass
    def parse_args(self):
        """
        This method is expected to behave identically as in the superclass,
        except that the sys.argv list will be pre-processed using
        _get_argv_after_doubledash before. See the docstring of the class for
        usage examples and details.
        """
        return super().parse_args(args=self._get_argv_after_doubledash())


if __name__=="__main__":
    argv = sys.argv
    argv = argv[argv.index("--")+1:]

    obj_file = argv[0]
    tex_file = argv[1]
    save_file = argv[2]
    csv_path = argv[3]
    if len(sys.argv)>4:
        multi_light = True

    # obj_file = "/home/aru/run5/100/objfile/obj1.obj"
    # tex_file = "/home/aru/run5/120/texture/1/tex1_r.png"
    # csv_path = "/home/aru/phd/objective2/dataset/compare/aoto/"

    deleteAllObjects()
#    addBackground()
    addBackgroundObj()
    b_mat = backgroundmat()
    deactivate_select()
    addBox(b_mat)
    csv_list_of_list = []

    # Add camera

    camera_data = bpy.data.cameras.new(name='Camera')
    camera_object = bpy.data.objects.new('Camera', camera_data)
    bpy.context.scene.collection.objects.link(camera_object)
    #bpy.data.objects["Camera"].rotation_euler = (0, 0, 0)
    csv_camera = [0,0,0.35]
    bpy.data.objects["Camera"].location = tuple(csv_camera)

    csv_camera_col = ["camera_x", "camera_y", "camera_z"]


    # Add light
    # addPointLight("PointLight1")
    addAreaLight("AreaLight")
    # lightNumber = 2

    # if multi_light:
    #     while random.randint(1,10)%2==0:
    #         lightName = "PointLight"+str(lightNumber)
    #         addPointLight(lightName)
    #         lightNumber +=1


    # Add object (use for loob to add all model subsiquently)

    imported_object = bpy.ops.import_scene.obj(filepath=obj_file)
    obj_object = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = obj_object
    object_name = obj_object.name
    activator(object_name)
    print('Imported name: ', obj_object.name)
    bpy.ops.object.shade_smooth()


    bpy.data.objects[object_name].scale = (0.001, 0.001, 0.001)

        # Random rotation

    x_rotation = np.clip(np.random.normal(scale=3.5), a_min=-5, a_max=5)
    y_rotation = random.uniform(-15,15)
    z_rotation = np.clip(np.random.normal(scale=5), a_min=-15, a_max=15)
    if random.random()>0.5:
        z_rotation += 180

    x_location = random.uniform(-0.04,0.04)
    y_location = random.uniform(-0.04,0.04)
    #z_location = random.uniform(-30,30)

    bpy.data.objects[object_name].rotation_euler = (math.radians(x_rotation), math.radians(y_rotation), math.radians(z_rotation))
    bpy.data.objects[object_name].location = (x_location, y_location, 0)
    csv_object = [x_rotation, y_rotation, z_rotation, x_location, y_location]
    csv_object_col = ["x_rotaiton", "y_ratation", "z_rotation", "x_location", "y_location"]

    # Texture to use (use glob and for loob to generate image for each crack texture)
    tex_path = tex_file
    mat = material1(tex_path)
    # pdb.set_trace()

    deactivate_select()
# Add second geometry

# File path
    parent_path = os.path.dirname(obj_file)
    base_name = os.path.basename(obj_file)
    obj2_file = parent_path+"/separate/"+base_name
    imported_object = bpy.ops.import_scene.obj(filepath=obj2_file)
    obj_object = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = obj_object
    object_name = obj_object.name
    activator(object_name)
    print('Imported name: ', obj_object.name)
    bpy.ops.object.shade_smooth()


    bpy.data.objects[object_name].scale = (0.001, 0.001, 0.001)

    #z_location = random.uniform(-30,30)

    bpy.data.objects[object_name].rotation_euler = (math.radians(x_rotation), math.radians(y_rotation), math.radians(z_rotation))
    bpy.data.objects[object_name].location = (x_location, y_location, 0)
    csv_object = [x_rotation, y_rotation, z_rotation, x_location, y_location]
    csv_object_col = ["x_rotaiton", "y_ratation", "z_rotation", "x_location", "y_location"]
    # material1(object_name, tex_path, mats_name    
    bpy.context.active_object.data.materials.clear()
    bpy.context.active_object.data.materials.append(mat)
    # Subdivide
    deactivate_select()


    ## Rending

    bpy.context.scene.render.filepath = save_file
#    bpy.data.scenes["Scene"].render.image_settings.file_format = "PNG"
    bpy.data.scenes["Scene"].render.image_settings.file_format = "OPEN_EXR"
    bpy.data.scenes["Scene"].render.resolution_y = 1024
    bpy.data.scenes["Scene"].render.resolution_x = 1024
    bpy.data.scenes["Scene"].render.engine = "CYCLES"
    bpy.data.scenes["Scene"].cycles.min_light_bounces = 3
    # bpy.data.scenes["Scene"].cycles.samples = 64
    bpy.data.scenes["Scene"].cycles.device = "GPU"
    csv_render = [1024, 1024]
    csv_render_col = ["resolution_x", "resolution_y"]
    csv_list = csv_camera + csv_object + csv_render
    csv_list.append(obj_file)
    csv_list.append(tex_file)
    csv_head = csv_camera_col + csv_object_col + csv_render_col
    csv_head.append("obj_file")
    csv_head.append("tex_file")
    csv_list_of_list.append(csv_head)
    csv_list_of_list.append(csv_list)
    csv_file_name = os.path.basename(save_file)
    writeFile = csv_path+csv_file_name+".csv"
    if writeFile:
       with open(writeFile, "w") as f:
           writer = csv.writer(f)
           writer.writerows(csv_list_of_list)

    bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)
    bpy.app.handlers.render_complete.append(some_other_function)



