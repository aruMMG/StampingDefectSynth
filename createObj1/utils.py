"""
Functions:
        
"""
import os
import re
import numpy as np
import random

def readLines(filePath):
    """
    input:
        filePath: path to the txt file to read lines from
        
    output:
        lines: list of strings. each strings is a line in the file
        
    """
    with open(filePath, "r") as f:
        lines = f.readlines()  
    return lines

def writeLines(filePath, lines):
    """
    inputs:
        filePath: path to txt file to write
        lines: list of strings to write in the file
        
    output:
        no return. write lines to the file
    
    """
    if os.path.exists(filePath):
        with open(filePath, "a") as f:
            for line in lines:
                f.write(line)
    else:
        with open(filePath, "w") as f:
            for line in lines:
                f.write(line)

def v_from_objLines(lines):

    v_list = []

    for line in lines:
        data = line.split()
        if data[0]=="v":
            v_list.append([float(data[1]), float(data[2]), float(data[3])])
    return v_list

def vt_from_objLines(lines):

    vt_list = []

    for line in lines:
        data = line.split()
        if data[0]=="vt":
            vt_list.append([float(data[1]), float(data[2])])
    return vt_list

def vn_from_objLines(lines):
    
    vn_list = []

    for line in lines:
        data = line.split()
        if data[0]=="vn":
            vn_list.append([float(data[1]), float(data[2]), float(data[3])])
    return vn_list

def f_from_objLines(lines, vt=False, vn=False):

    f_list = []

    for line in lines:
        data = line.replace("/", " ")
        data = data.split()
        if data[0]=="f":
            if len(data)>7:
                if vt and vn:
                    f_list.append([int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]), int(data[7]), int(data[8]), int(data[9])])
                elif vt:
                    f_list.append([int(data[1]), int(data[2]), int(data[4]), int(data[5]), int(data[7]), int(data[8])])
                elif vn:
                    f_list.append([int(data[1]), int(data[3]), int(data[4]), int(data[6]), int(data[7]), int(data[9])])
                else:
                    f_list.append([int(data[1]), int(data[4]), int(data[7])])
            elif len(data)>4:
                if vt or vn:
                    f_list.append([int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6])])
                else:
                    f_list.append([int(data[1]), int(data[3]), int(data[5])])
            else:
                f_list.append([int(data[1]), int(data[2]), int(data[3])])
    return f_list

def v_write(filePath, v_list):
    """
    inputs:
        filePath: path to txt file to write
        v_list: list of list for vertices to write in the file
        
    output:
        no return. write lines to the file
    
    """
    if os.path.exists(filePath):
        with open(filePath, "a") as f:
            for l in v_list:
                f.write("v %.4f %.4f %.4f\n" % tuple(l))
    else:
        with open(filePath, "w") as f:
            for l in v_list:
                f.write("v %.4f %.4f %.4f\n" % tuple(l))

def vt_write(filePath, vt_list):
    """
    inputs:
        filePath: path to txt file to write
        vt_lines: list of list for textures to write in the file
        
    output:
        no return. write lines to the file
    
    """
    if os.path.exists(filePath):
        with open(filePath, "a") as f:
            for l in vt_list:
                f.write("vt %.4f %.4f\n" % tuple(l))
    else:
        with open(filePath, "w") as f:
            for l in vt_list:
                f.write("vt %.4f %.4f\n" % tuple(l))

def vn_write(filePath, n_list):
    """
    inputs:
        filePath: path to txt file to write
        vn_lines: list of list for normals to write in the file
        
    output:
        no return. write lines to the file
    
    """
    if os.path.exists(filePath):
        with open(filePath, "a") as f:
            for l in n_list:
                f.write("vn %.4f %.4f %.4f\n" % tuple(l))
    else:
        with open(filePath, "w") as f:
            for l in n_list:
                f.write("vn %.4f %.4f %.4f\n" % tuple(l))

def f_write(filePath, f_list, n=1):
    """
    inputs:
        filePath: path to txt file to write
        f_lines: list of list for face ("f") to write in the file
        n: int. is equal to 1 if only vertex used, 2 if vetex and texture used, 3 for normal use
        
    output:
        no return. write lines to the file
    
    """
    n=len(f_list[0])
    if os.path.exists(filePath):
        with open(filePath, "a") as f:
            if n==2:
                for l in f_list:
                    f.write("f %d/%d %d/%d %d/%d\n" % tuple(l))
            if n==3:
                for l in f_list:
                    f.write("f %d/%d/%d %d/%d/%d %d/%d/%d\n" % tuple(l))
            else:
                for l in f_list:
                    f.write("f %d %d %d\n" % tuple(l))
    else:
        with open(filePath, "w") as f:
            if n==2:
                for l in f_list:
                    f.write("f %d/%d %d/%d %d/%d\n" % tuple(l))
            if n==3:
                for l in f_list:
                    f.write("f %d/%d/%d %d/%d/%d %d/%d/%d\n" % tuple(l))
            else:
                for l in f_list:
                    f.write("f %d %d %d\n" % tuple(l))

def v_in_limit(lines, coordLimit):
    vertex_list = v_from_objLines(lines)
    x_min, x_max, y_min, y_max, z_min, z_max = coordLimit

    v_limit = []
    for (x, y, z) in vertex_list:
        if x_min<x<x_max and y_min<y<y_max and z_min<z<z_max:
            v_limit.append([x,y,z])
    return v_limit

def coordToNode(v_list):
    coordToNode_dict = {}
    node_num = 0
    for l in v_list:
        node_num += 1
        coordToNode_dict[tuple(l)] = node_num
    return coordToNode_dict

def randomPoly():
    """
    """
    # x0 = 0.2*np.random.rand(1)[0]
    x0 = 0*np.random.rand(1)[0]
    # x5 = 0.2*np.random.rand(1)[0]
    x5 = 0.2

    # x1 = 0.2*np.random.rand(1)[0]
    x1 = 0*np.random.rand(1)[0]
    return np.polyfit((0,0.5,1),(x0,x5,x1), deg=2)

def deviateUV(vt, cross=False, reverse=False):
    polyArr = randomPoly()
    # print(np.polyval(polyArr, (0,0.3, 0.5, 0.8,1)))
    # print(vt[100,:])
    if cross:
        if random.random()<0.5:
            vt[:,1] -= np.polyval(polyArr, vt[:,0])
        else:
            vt[:,1] += np.polyval(polyArr, vt[:,0])
    else:
        if reverse:
            vt[:,0] -= np.polyval(polyArr, vt[:,1])
        else:
            vt[:,0] += np.polyval(polyArr, vt[:,1])

    for i in range(vt.shape[0]):
        for j in range(vt.shape[1]):
            if vt[i,j]<0.02:
                vt[i,j]=0.02
            elif vt[i,j]>0.98:
                vt[i,j]=0.98

    # vt = np.clip(vt, 0,1)
    # print(vt[100,:])
    return vt


if __name__=="__main__":
    arr = randomPoly()
    print(arr)