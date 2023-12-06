from addNoDefect import addNoDefect
import numpy as np
import matplotlib.pyplot as plt

from createobj_utils import checkDefect, cleanElemData, cleanStrainData, cleanCoordData, cluster_DBSCAN, textureMap1
from utils import deviateUV

#  bring a dictionary similar to noDefect_dict for defect one and copy from there.
def createObj(args, coordDF, nodesTOcoord_dict, coordTOnodes_dict, nodes_DynaToObj_dict, nodes_ObjToDyna_dict, elemDF, defect_data, objNum, texRatio, texSize, one_defect=True):

    defect_elem_dict = {}
    f_NoDefect_list = []
    noDefect_elem_dict = {}

    Falsecount = 0
    Truecount = 0

    for idx, row in elemDF.iterrows():
        nodes = (int(row["Node1"]), int(row["Node2"]), int(row["Node3"]), int(row["Node4"]))
        
        tul = []
        # write f in obj file for non defective elements.
        if row["Elem_ID"] in defect_data:
            Truecount+=1
            defect_elem_dict[int(row["Elem_ID"])] = list(nodes)
        else:

            Falsecount += 1
            noDefect_elem_dict[int(row["Elem_ID"])] = list(nodes)
            for i in nodes:
                tul.append(nodes_DynaToObj_dict[int(i)])
            
            # Store f values for no defect elements in a list
            f_NoDefect_list.append((tul[0], 1, tul[1], 1, tul[2], 1))
            f_NoDefect_list.append((tul[0], 1, tul[2], 1, tul[3], 1))

            # Write f values for no defect elements in to obj file
            # f.write("f %d/%d %d/%d %d/%d\n" % (tul[0], 1, tul[1], 1, tul[2]), 1)
            # f.write("f %d/%d %d/%d %d/%d\n" % (tul[0], 1, tul[2], 1, tul[3]), 1)
    total_elem_dyna = Truecount + Falsecount
    assert total_elem_dyna==len(noDefect_elem_dict) + len(defect_elem_dict), "number of elements mmismatched"

    # "Elem_ID", "node1", "node2", "node3", "node4" and "cluster"
    defect_elem_df = cluster_DBSCAN(defect_elem_dict, nodesTOcoord_dict)
    defect_clusters_dict = dict(tuple(defect_elem_df.groupby('cluster')))

    # Remove both unwanted defect
    ignore_defect_dict = {}
    if -1 in defect_clusters_dict:
        ignore_defect_dict[-1] = defect_clusters_dict[-1]
        defect_clusters_dict.pop(-1)
    if args.sample_size==40 or args.sample_size==80:
        ignore_defect_dict[0] = defect_clusters_dict[0]
        defect_clusters_dict.pop(0)
    if  args.sample_size==170 and args.fullDefect:
        ignore_defect_dict[0] = defect_clusters_dict[0]
        defect_clusters_dict.pop(0)
    if args.sample_size==140:
        ignore_defect_dict[1] = defect_clusters_dict[1]
        defect_clusters_dict.pop(1)


    for key, ignore_df in ignore_defect_dict.items():
        for idx, row in ignore_df.iterrows():
            nodes = (int(row["Node1"]), int(row["Node2"]), int(row["Node3"]), int(row["Node4"]))
            noDefect_elem_dict[int(row["Elem_ID"])] = list(nodes)
            defect_elem_dict.pop(int(row["Elem_ID"]))
    assert total_elem_dyna==len(noDefect_elem_dict) + len(defect_elem_dict), "number of elements mmismatched"

    if not args.sample_size==120:
        defect_elem_len = 0
        for key in defect_clusters_dict:
            one_cluster_df = defect_clusters_dict[key]
            defect_elem_len += one_cluster_df.shape[0]
            assert len(defect_elem_dict)==defect_elem_len, "numbeer of defective elements mismatch with defect dictionary"


    ClusterNodeToVtNum_dict = {}
    defect_elem_len = 0
    f_Defect_list = []
    for key in defect_clusters_dict:
        
        coordList = []
        nodes_set = set()
        one_cluster_df = defect_clusters_dict[key]
        defect_elem_len += one_cluster_df.shape[0]
        for idx, row in one_cluster_df.iterrows():
            for i in range(1,5):
                if row.iloc[i] not in nodes_set:
                    nodeCoord = list(nodesTOcoord_dict[int(row.iloc[i])])
                    coordList.append(nodeCoord)
                    nodes_set.add(row.iloc[i])

        # PCA
        coordArr = np.array(coordList)
        coordArr, one_cluster_df, noDefect_elem_dict = addNoDefect(args, coordArr, coordDF, noDefect_elem_dict, defect_elem_dict, one_cluster_df, coordTOnodes_dict, nodesTOcoord_dict, nodes_ObjToDyna_dict, key)
        # coord_PCA,_ = pca.pca2(coordArr)
        # largest_face = coord_PCA[:,[0,1]]
        largest_face = coordArr[:,[0,1]]

        vt = textureMap1(largest_face) # array of size largest_face.shape (m,2)
        assert coordArr.shape[0]==vt.shape[0]
        vt = deviateUV(vt)

        fig,ax = plt.subplots(2)
        ax[0].scatter(coordArr[:,0], coordArr[:,2], c="red")

        ax[1].scatter(vt[:,0], vt[:,1], c="green")

        plt.savefig("images/coordplot_noPCA_{}_02.png".format(key))
        
        with open("{}/separate/obj{}.obj".format(args.save_dir, objNum), "w") as f:
            # f.write("mtllib texture.mtl\n")
            coordDF.sort_values(["Node_ID_obj"])
            for idx,row in coordDF.iterrows():
                f.write("v %.4f %.4f %.4f\n" % (float(row["Coord1"]), float(row["Coord2"]), float(row["Coord3"])))
            
            f.write("vt %.5f %.5f\n" %(0,0))
            
            for i in range(coordArr.shape[0]):
                f.write("vt %.5f %.5f\n" % (vt[i,0], vt[i,1]))
                node_obj = coordTOnodes_dict[tuple(coordArr[i,:])]
                ClusterNodeToVtNum_dict[(key, node_obj)] = i+2 # make a dict node of cluster to vt_num

            # one_cluster_df = defect_clusters_dict[key]
            f.write("usemtl \n")
            for idx, row in one_cluster_df.iterrows():
                nodes = tuple([int(row.iloc[i]) for i in range(1,5)])
                tul = []
                tul_vt = []
                for i in nodes:
                    node_obj = nodes_DynaToObj_dict[i]
                    tul.append(node_obj)
                    tul_vt.append(ClusterNodeToVtNum_dict[(key, node_obj)])
                
                f.write("f %d/%d %d/%d %d/%d\n" % (tul[0], tul_vt[0], tul[1], tul_vt[1], tul[2], tul_vt[2]))
                f.write("f %d/%d %d/%d %d/%d\n" % (tul[0], tul_vt[0], tul[2], tul_vt[2], tul[3], tul_vt[3]))
    with open("{}/obj{}.obj".format(args.save_dir,objNum), "w") as f:
        coordDF.sort_values(["Node_ID_obj"])
        for idx,row in coordDF.iterrows():
            f.write("v %.4f %.4f %.4f\n" % (float(row["Coord1"]), float(row["Coord2"]), float(row["Coord3"])))
            
        f_NoDefect_list = []
        for key, val in noDefect_elem_dict.items():
            tul = []
            for i in val:
                tul.append(nodes_DynaToObj_dict[i])
            f_NoDefect_list.append((tul[0], tul[1], tul[2]))
            f_NoDefect_list.append((tul[0], tul[2], tul[3]))


        for elem in f_NoDefect_list:
            f.write("f %d %d %d\n" % (elem[0], elem[1], elem[2]))


    # f.write("usemtl {}\n".format("nodefectMtl"))
    # for elem in f_NoDefect_list:
    #     f.write("f %d/%d %d/%d %d/%d\n" % (elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))
    # for elem in f_Defect_list:
    #     if type(elem) == str:
    #         f.write("usemtl {}\n".format(elem))
    #     else:
    #         f.write("f %d/%d %d/%d %d/%d\n" % (elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))

def loop(args, coordDF, nodesTOcoord_dict, coordTOnodes_dict, nodes_DynaToObj_dict, nodes_ObjToDyna_dict, elemDF, defect_data):
    # texture_path = "/home/aru/phd/objective2/blender/blendFile/texture/textureRaw/*.png"
    objNum = 0
    # for tex_name in glob.glob(texture_path):
    for variation in range(args.size):
        objNum+=1
        # tex_img = cv2.imread(tex_name)
        # texSize = np.array([tex_img.shape[1],tex_img.shape[0]])
        texRatio = False
        createObj(args, coordDF, nodesTOcoord_dict, coordTOnodes_dict, nodes_DynaToObj_dict, nodes_ObjToDyna_dict, elemDF, defect_data, objNum, texRatio, texSize=(300,600))

if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Progressive Growing of GANs')
    parser.add_argument('--save_dir', type=str, default='objfile', help='Save directory obj file')
    parser.add_argument('--coord_DF', type=str, default='./dynaFile/40/coord4', help='Dyna data for coordinates')
    parser.add_argument('--elem_DF', type=str, default='./dynaFile/40/elem4', help='Dyna data for elements')
    parser.add_argument('--strain_DF', type=str, default='./dynaFile/40/strain4', help='Dyna data for strain')

    parser.add_argument('--plotStrain', action='store_true', help='Is it a baseline corected data.')
    parser.add_argument('--FullLength', action='store_true', help='Is the defect cove full length of part.')

    parser.add_argument('--writeDefect', default="", type=str, help='write the defect element to a csv file')
    parser.add_argument('--size', default=10, type=int, help='The number of obj files to generate')
    parser.add_argument('--sample_size', default=40, type=int, help='The width of nakajima sample')
    args = parser.parse_args()


    # clean coord data
    # "Node_ID_obj", "Node_ID", "Coord1", "Coord2", "Coord3"
    coordDF, nodesTOcoord_dict, coordTOnodes_dict, nodes_DynaToObj_dict, nodes_ObjToDyna_dict = cleanCoordData(args.coord_DF)

    # clean element data
    # "Elem_ID", "Part_ID", "Node1", "Node2", "Node3", "Node4"
    elemDF = cleanElemData(args.elem_DF)
    elemID = elemDF["Elem_ID"].tolist()
    elemRange = (int(max(elemID)), int(min(elemID)))

    # clean strain data
    # "Elem_ID", "Lower_Major", "Lower_Minor", "Upper_Major", "Upper_Minor", "Thickness", "Reduction"
    strainDF = cleanStrainData(args.strain_DF, elemRange)

    # check for defect data
    defect_df = checkDefect(args, strainDF)
    d = dict(tuple(defect_df.groupby('Lcrack'))) # dictionary with key 1 for defect and 0 for safe element

    defect_data = d[1]["Elem_ID"].tolist()
    loop(args, coordDF, nodesTOcoord_dict, coordTOnodes_dict, nodes_DynaToObj_dict, nodes_ObjToDyna_dict, elemDF, defect_data)
    # createObj(coordDF, nodesTOcoord_dict, coordTOnodes_dict, nodes_DynaToObj_dict, nodes_ObjToDyna_dict, elemDF, defect_data, objFileName="/home/aru/phd/objective2/blender/blendFile/geometry/check", objNum=1, texRatio=False, texSize=(300,600))
