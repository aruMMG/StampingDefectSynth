from statistics import NormalDist
import numpy as np
from collections import defaultdict

from utils import f_from_objLines, f_write, readLines, v_from_objLines, v_write, writeLines, vt_from_objLines, vt_write, n_write


def normalize(v):
    return v/np.linalg.norm(v)

def sum_normalize(l):
    return l/sum(l)

def vertex_normal(vertices, faces, normal_direction):  
    vertex_face_normal = defaultdict(list)
    count=0
    for i in range(faces.shape[0]):
        count+=1
        face = faces[i,:]
        v1_idx, v2_idx, v3_idx = tuple(face)
        v1 = vertices[v1_idx-1,:]
        v2 = vertices[v2_idx-1,:]
        v3 = vertices[v3_idx-1,:]

        normal = np.cross(v2-v1, v3-v1)
        angle = np.arccos(np.dot(normalize(normal), normalize(normal_direction)))
        if angle>(np.pi/2):
            normal = -1 * normal
        vertex_face_normal[tuple(v1)].append(normal)
        vertex_face_normal[tuple(v2)].append(normal)
        vertex_face_normal[tuple(v3)].append(normal)
    smooth_normal = {}
    print(count)
    for v, normals in vertex_face_normal.items():
        normals_lens = [np.linalg.norm(x) for x in normals]
        weights = sum_normalize(normals_lens)
        weighted_normal = np.array([weights[i]*normals[i] for i in range(len(normals))])
        normal = sum(weighted_normal)
        smooth_normal[v] = normal
    return smooth_normal

def obj_vetex_normal(objFile, objFileWithVT, normal_direction=np.array([0,1,0])):
    """
    Smooth normal, first calculate face normal then calculate weighted vertex normal
    """
    lines = readLines(objFile)
    vertices = np.array(v_from_objLines(lines))
    vt = vt_from_objLines(lines)
    faces = f_from_objLines(lines)
    smooth_normal = vertex_normal(vertices, np.array(faces), normal_direction)
    
    vn = []
    v_num=0
    v_to_vn = {}
    for i in range(vertices.shape[0]):
        v = vertices[i,:]
        if tuple(v) in smooth_normal:
            v_num+=1
            v_to_vn[i+1] = v_num
            vn.append(smooth_normal[tuple(v)])


    v_write(objFileWithVT, list(vertices))
    vt_write(objFileWithVT, vt)
    n_write(objFileWithVT, vn)

    with open(objFileWithVT, "a") as g:
        for line in lines:
            data = line.split()
            if data[0]=="f":
                data = line.replace("/", " ")
                data = data.split()
                g.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(data[1], data[2], v_to_vn[int(data[1])], data[3], data[4], v_to_vn[int(data[3])], data[5], data[6], v_to_vn[int(data[5])]))




if __name__=="__main__":
    objFile = "/home/aru/phd/objective2/python/python/python/createOBJ/objFile/separate/texture_visualiseR2.obj"
    objout = "/home/aru/phd/objective2/python/python/python/createOBJ/objFile/separate/texture_visualiseR2_vn0.5PI_z.obj"
    obj_vetex_normal(objFile, objout, np.array([0, 0, 1]))
