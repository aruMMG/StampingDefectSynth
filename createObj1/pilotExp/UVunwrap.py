import imp
import utils
import os
import numpy as np
import pca
from textureMapping import textureMap1

def calculatePercent(m, texture_size):
    mini = np.min(m, axis=0)
    maxi = np.max(m, axis=0)
    map_size = maxi-mini
    percent = map_size/texture_size
    return tuple(percent)

def coordLimit(coordFile_dyna, elemFile_dyna, strainFile):
        # clean coord data
    _, nodesTOcoord_dict, _,_,_ = cleanToCsv.cleanCoordData(coordFile_dyna)    # Dyna node and coordinates

    # clean element data
    # "Elem_ID", "Part_ID", "Node1", "Node2", "Node3", "Node4" 
    elemDF = cleanToCsv.cleanElemData(elemFile_dyna)    # All dyna
    elemID = elemDF["Elem_ID"].tolist()
    elemRange = (int(max(elemID)), int(min(elemID)))
    # clean strain data
    # "Elem_ID", "Lower_Major", "Lower_Minor", "Upper_Major", "Upper_Minor", "Thickness", "Reduction"
    strainDF = cleanToCsv.cleanStrainData(strainFile, elemRange)

    # check for defect data
    defect_df = check.checkDefect(strainDF)
    d = dict(tuple(defect_df.groupby('Lcrack'))) # dictionary with key 1 for defect and 0 for safe element

    defect_data = d[1]["Elem_ID"].tolist()

    defect_elem_dict = {}
    noDefect_elem_dict = {}

    Falsecount = 0
    Truecount = 0

    for idx, row in elemDF.iterrows():
        nodes = (int(row["Node1"]), int(row["Node2"]), int(row["Node3"]), int(row["Node4"]))
        
        # write f in obj file for non defective elements.
        if row["Elem_ID"] in defect_data:
            Truecount+=1
            defect_elem_dict[int(row["Elem_ID"])] = list(nodes)
        else:
            Falsecount+=1
            noDefect_elem_dict[int(row["Elem_ID"])] = list(nodes)
    
    # "Elem_ID", "node1", "node2", "node3", "node4" and "cluster"
    defect_elem_df = cluster.cluster_DBSCAN(defect_elem_dict, nodesTOcoord_dict)
    defect_clusters_dict = dict(tuple(defect_elem_df.groupby('cluster')))
    # Remove both unwanted defect
    defect_clusters_dict.pop(0)
    defect_clusters_dict.pop(2)


    for key in defect_clusters_dict:
        coordList, coord_limits = [], []
        nodes_set = set()
        one_cluster_df = defect_clusters_dict[key]
        for idx, row in one_cluster_df.iterrows():
            for i in range(1,5):
                if row.iloc[i] not in nodes_set:
                    nodeCoord = list(nodesTOcoord_dict[int(row.iloc[i])])
                    coordList.append(nodeCoord)
                    nodes_set.add(row.iloc[i])
        
        coordArr = np.array(coordList)
        minx,miny,minz =  np.min(coordArr, axis=0)
        maxx,maxy,maxz =  np.max(coordArr, axis=0)
        coord_limit = (minx, maxx, minz, maxz, miny, maxy)
        coord_limits.append(coord_limit)
    return coord_limits

def print_V_limit(v_list):
    v_arr = np.array(v_list)
    min0,min1,min2 =  np.min(v_arr, axis=0)
    max0,max1,max2 =  np.max(v_arr, axis=0)
    coord_limit = (min0, max0, min1, max1, min2, max2)
    print(coord_limit)

def UVunwrap(file_path, coord_limit, write_path):
    """
    input: 
        file_path: String, file location of obj file
        coord_limit: tuple (x_min, x_max, z_min, z_max, y_min, y_max), minimum and maximum coordinate value
        write_path: path to save the modified obj file
    output:
        write obj file with UV unwraped to write_path 
    """
    if write_path:
        pass
    else:
        write_path = os.path.dirname(file_path)

    lines = utils.readLines(file_path)
    vertices_in_limit = np.array(utils.v_in_limit(lines,coord_limit))
    coord_PCA,_ = pca.pca2(vertices_in_limit)
    largest_face = coord_PCA[:,[0,2]]
    percent = calculatePercent(largest_face, np.array([40,20]))
    vt = textureMap1(largest_face, percent)

    v_list = utils.v_from_objLines(lines)
    vn_list = utils.vn_from_objLines(lines)
    f_list = utils.f_from_objLines(lines, vn=True, vt=True)

    utils.v_write(write_path, v_list)

    coordTOnodes_dict = utils.coordToNode(v_list)
    nodeToVtIdx_dict = {}

    with open(write_path, "a") as f:
        vt_count = 1
        f.write("vt %.5f %.5f\n" % (0.00, 0.00))
        for i in range(vertices_in_limit.shape[0]):
            f.write("vt %.5f %.5f\n" % (vt[i,0], vt[i,1]))
            vt_count+=1
            node_obj = coordTOnodes_dict[tuple(vertices_in_limit[i,:])]
            nodeToVtIdx_dict[node_obj] = vt_count

    utils.vn_write(write_path, vn_list)

    with open(write_path, "a") as f:
        for f_vn_list in f_list:
            f_tuple = []
            for i in range(6):
                if i%2==0:
                    f_tuple.append(f_vn_list[i])
                    if f_vn_list[i] in nodeToVtIdx_dict:
                        vt_idx = nodeToVtIdx_dict[f_vn_list[i]]
                    else:
                        vt_idx = 1
                    f_tuple.append(vt_idx)
                else:
                    f_tuple.append(f_vn_list[i])
            f.write("f %d/%d/%d %d/%d/%d %d/%d/%d\n" % tuple(f_tuple))                

import cleanToCsv
import check
import cluster

if __name__=="__main__":

    coordFile_dyna = "/home/aru/phd/objective2/FEM_files/LDH_model/LDH_model/Test10/stage4_blank_coord.txt"
    elemFile_dyna = "/home/aru/phd/objective2/FEM_files/LDH_model/LDH_model/Test10/stage_blank_elem.txt"
    strainFile = "/home/aru/phd/objective2/FEM_files/LDH_model/LDH_model/Test10/strain4"

    coord_limits = coordLimit(coordFile_dyna, elemFile_dyna, strainFile)
    print(coord_limits[0])

    obj_fiile_path = "/home/aru/phd/objective2/blender/blendFile/geometry/subdivide.obj"
    write_path = "/home/aru/phd/objective2/blender/blendFile/geometry/subdivideUVunwarp.obj"

    UVunwrap(obj_fiile_path, coord_limit=coord_limits[0], write_path=write_path)

