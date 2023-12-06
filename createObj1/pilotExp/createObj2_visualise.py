from addNodefects40 import addNoDefect
import numpy as np
import matplotlib.pyplot as plt

from createobj_utils import checkDefect, cleanElemData, cleanStrainData, cleanCoordData, cluster_DBSCAN, textureMap1, pca2
from utils import deviateUV


def createObj(args, coordDF, nodesTOcoord_dict, coordTOnodes_dict, nodes_DynaToObj_dict, nodes_ObjToDyna_dict, elemDF, defect_data, texRatio, texSize):
    defect_elem_dict = {}
    noDefect_elem_dict = {}
    colours = ["Red", "Blue", "Green", "Black", "RedBlue", "BlueGreen", "GreenRed"]
    with open(args.save_dir, "w") as f:
        f.write("mtllib check.mtl\n")
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
        
        # Write v values in obj file.
        coordDF.sort_values(["Node_ID_obj"])
        for idx,row in coordDF.iterrows():
            f.write("v %.4f %.4f %.4f\n" % (float(row["Coord1"]), float(row["Coord2"]), float(row["Coord3"])))
        
        # Write vt for no defect elements
        # One v for all the no defect elements
        f.write("vt %.5f %.5f\n" %(0,0))
        ClusterNodeToVtNum_dict = {}
        f_Defect_list = []
        
        # "Elem_ID", "node1", "node2", "node3", "node4" and "cluster"
        defect_elem_df = cluster_DBSCAN(defect_elem_dict, nodesTOcoord_dict)
        defect_clusters_dict = dict(tuple(defect_elem_df.groupby('cluster')))
        # # Remove both unwanted defect
        # ignore_defect_dict = {}
        # ignore_defect_dict[0] = defect_clusters_dict[0]
        # ignore_defect_dict[1] = defect_clusters_dict[1]
        # ignore_defect_dict[2] = defect_clusters_dict[2]
        # defect_clusters_dict.pop(0)
        # defect_clusters_dict.pop(1)
        # defect_clusters_dict.pop(2)


        # for key, ignore_df in ignore_defect_dict.items():
        #     for idx, row in ignore_df.iterrows():
        #         nodes = (int(row["Node1"]), int(row["Node2"]), int(row["Node3"]), int(row["Node4"]))
        #         noDefect_elem_dict[int(row["Elem_ID"])] = list(nodes)
        # Removed



        for key in defect_clusters_dict:
            coordList = []
            nodes_set = set()
            one_cluster_df = defect_clusters_dict[key]
            for idx, row in one_cluster_df.iterrows():
                for i in range(1,5):
                    if row.iloc[i] not in nodes_set:
                        nodeCoord = list(nodesTOcoord_dict[int(row.iloc[i])])
                        coordList.append(nodeCoord)
                        nodes_set.add(row.iloc[i])

            # PCA
            coordArr = np.array(coordList)
            # coordArr, one_cluster_df, noDefect_elem_dict = addNoDefect(coordArr, coordDF, noDefect_elem_dict, one_cluster_df, nodes_ObjToDyna_dict, key)
            
            defect_clusters_dict[key] = one_cluster_df
            coord_PCA,_ = pca2(coordArr)
            # largest_face = coord_PCA[:,[0,1]]


            # largest_face = np.flip(largest_face, axis=0)
            # largest_face = np.flip(largest_face, axis=1)


            largest_face = coordArr[:,[0,1]]
            # if key==1:
            #     theta = np.radians(180)
            #     c,s = np.cos(theta), np.sin(theta)
            #     rotation_matrix = np.array([[c,-s],[s,c]])
            #     largest_face = np.matmul(largest_face,rotation_matrix)
            

            # theta = np.radians(-60)
            # c,s = np.cos(theta), np.sin(theta)
            # rotation_matrix = np.array([[c,-s],[s,c]])
            # largest_face = np.matmul(largest_face,rotation_matrix)

            fig,ax = plt.subplots(4)
            ax[0].scatter(largest_face[:,0], largest_face[:,1], c="red")

            vt = textureMap1(largest_face, texRatio, texSize) # array of size largest_face.shape (m,2)
            ax[1].scatter(vt[:,0], vt[:,1], c="green")
            vt = deviateUV(vt)
            ax[2].scatter(vt[:,0], vt[:,1], c="green")
            # vt = textureMap1(vt, texRatio, texSize)
            ax[3].scatter(vt[:,0], vt[:,1], c="green")
            assert coordArr.shape[0]==vt.shape[0]


            plt.savefig("images/coordplot_PCA2R15_{}.png".format(key))
            
            for i in range(coordArr.shape[0]):
                f.write("vt %.5f %.5f\n" % (vt[i,0], vt[i,1]))
                node_obj = coordTOnodes_dict[tuple(coordArr[i,:])]
                ClusterNodeToVtNum_dict[(key, node_obj)] = i+2 # make a dict node of cluster to vt_num
        for key in defect_clusters_dict:
            one_cluster_df = defect_clusters_dict[key]
            f_Defect_list.append(colours[key+1])
            for idx, row in one_cluster_df.iterrows():
                nodes = tuple([int(row.iloc[i]) for i in range(1,5)])
                tul = []
                tul_vt = []
                for i in nodes:
                    node_obj = nodes_DynaToObj_dict[i]
                    tul.append(node_obj)
                    tul_vt.append(ClusterNodeToVtNum_dict[(key, node_obj)])
                f_Defect_list.append((tul[0], tul_vt[0], tul[1], tul_vt[1], tul[2], tul_vt[2]))
                f_Defect_list.append((tul[0], tul_vt[0], tul[2], tul_vt[2], tul[3], tul_vt[3]))
        
        # f.write("usemtl {}\n".format("nodefectMtl"))

        f_NoDefect_list = []
        for key, val in noDefect_elem_dict.items():
            tul = []
            for i in val:
                tul.append(nodes_DynaToObj_dict[i])
            f_NoDefect_list.append((tul[0], 1, tul[1], 1, tul[2], 1))
            f_NoDefect_list.append((tul[0], 1, tul[2], 1, tul[3], 1))

        f.write("usemtl Default_OBJ\n")
        for elem in f_NoDefect_list:
            f.write("f %d/%d %d/%d %d/%d\n" % (elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))
        for elem in f_Defect_list:
            if type(elem) == str:
                # pass
                f.write("usemtl {}\n".format(elem))
            else:
                f.write("f %d/%d %d/%d %d/%d\n" % (elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))


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
    createObj(args, coordDF, nodesTOcoord_dict, coordTOnodes_dict, nodes_DynaToObj_dict, nodes_ObjToDyna_dict, elemDF, defect_data, texRatio=False, texSize=(300,600))
