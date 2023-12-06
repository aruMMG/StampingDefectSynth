import pandas as pd
import matplotlib.pyplot as plt
import numpy
import csv
from sklearn.cluster import DBSCAN
import numpy as np
from utils import randomPoly

def checkDefect(args, df, objective=None, writeFile=None):# 60 - 2.5, 40 - 17, 100 - 10, 80 - 0, 120 - 10, 140 - 10, full - 5 For 40 and 60 the addefect file is changed
    if not objective:    
        def objective(x, a=args.a): # 60 - 2.5, 40 - 17, 100 - 10, 80 - 0, 120 - 10, 140 - 10, full - 5 For 40 and 60 the addefect file is changed
            if x>0:
                return a+0.6*x
            else:
                return a+0.5*abs(x)
    if args.plotStrain:
    # plot lower strain
        fig, ax = plt.subplots(figsize = (8,8))
        ax.scatter(df.Lower_Minor, df.Lower_Major,)
        plt.xlabel("Minir_strain")
        plt.ylabel("Major_strain")
        plt.savefig("lowerStrain4.png")

        # plot upper strain
        fig, ax = plt.subplots(figsize = (8,8))
        ax.scatter(df.Upper_Minor, df.Upper_Major,)
        plt.xlabel("Minir_strain")
        plt.ylabel("Major_strain")
        plt.savefig("upperStrain4.png")


    Lcrack = []
    Ucrack = []
    for index, row in df.iterrows():
        Lx = float(row["Lower_Minor"])
        Ly = float(row["Lower_Major"])
        Ux = float(row["Upper_Minor"])
        Uy = float(row["Upper_Major"])

        if objective(Lx) < Ly:
            Lcrack.append(1)
        else:
            Lcrack.append(0)

        if objective(Ux) < Uy:
            Ucrack.append(1)
        else:
            Ucrack.append(0)

    df["Lcrack"] = Lcrack
    df["Ucrack"] = Ucrack
    if writeFile:
        df.to_csv(writeFile)
    
    return df



def cleanElemData(fileToClean):

    """
    input: Take file path for the file from LSDYNA containing Element ID and node information
    
    OutPut: A dataframe with same data
    """
    elemDFListOfList = []
    with open(fileToClean, "r") as f:
        lines = f.readlines()
        dataStart = False
        for line in lines:
            if line == "*ELEMENT_SHELL\n":
                dataStart = True
                continue
            if dataStart == True:
                data = line.split()
                if data[0] == "*END" or data[0] == "*END\n":
                    break
                elemDFListOfList.append(data)
    return pd.DataFrame(elemDFListOfList, columns=["Elem_ID", "Part_ID", "Node1", "Node2", "Node3", "Node4"])


def cleanStrainData(fileToClean, ElemIDRange, writeFile=None):
    """
    Inputs:
        fileToClean: file path of strain data from LSDYNA to clean.
        ElemIDRange: tuple of size (1,2) contain the lowest and highest elementID
        writeFile: The file path if required to write the clean data to a csv file

    Output:
        df: a dataframe column containing Elem_ID, strain and few other data
    """
    writeLine = False
    listOfListOfData = []
    with open(fileToClean) as f:
        lines = f.readlines()
        for line in lines:
            dataInLine = line.split()
            if dataInLine[0]=="$Elem":
                writeLine=True
                continue
            if writeLine==True:
                try:
                    first_elem = int(dataInLine[0])
                    if first_elem>=ElemIDRange[1] and first_elem<=ElemIDRange[0]:
                        listOfListOfData.append(dataInLine)
                except ValueError:
                    print("The elementID is: {}, but the range of ID is {}".format(dataInLine[0], ElemIDRange))
    if writeFile:
        with open(writeFile, "w") as g:
            writer = csv.writer(g)
            writer.writerows(listOfListOfData)
    
    return pd.DataFrame(listOfListOfData, columns=["Elem_ID", "Lower_Major", "Lower_Minor", "Upper_Major", "Upper_Minor", "Thickness", "Reduction"])

def cleanCoordData(filename, writeFile=None):
    """
    Inputs:
        filename: file path containing coordinate of vertex from LSDyna
        writeFile: file path if present save the data cleaned csv data to this file
    
    outputs:
        df: dataframe with columns "Node_ID_obj", "Node_ID", "Coord1", "Coord2", "Coord3".
        node_coord_dict: dictionary {node_dyna: tuple_of_coordinate}
        nodes_DynaToObj_dict: dictionary {node_dyna: Node_ID_obj}
        nodes_ObjToDyna_dict: dictionary {Node_ID_obj: node_dyna}
    
    
    """

    nodes_DynaToObj_dict = {} # dictionary {node_dyna: node_sequence_for_obj}
    nodes_ObjToDyna_dict = {}
    coordTOnodes_dict = {}
    nodesTOcoord_dict = {} # dictionary {node_dyna: tuple_of_coordinate}
    listOfListData = []
    with open(filename, "r") as f:
        lines = f.readlines()
        dataStart = False
        node_num = 0
        for line in lines:
            if line == "*NODE\n":
                dataStart = True
                continue
            if dataStart == True:
                data = line.split()
                if data[0] == "*END" or data[0] == "*END\n":
                    break
                
                node_Dyna = int(data[0])
                node_num += 1
                nodes_DynaToObj_dict[node_Dyna] = node_num
                nodes_ObjToDyna_dict[node_num] = node_Dyna
                coord_tuple = tuple(map(float, data[1:]))
                nodesTOcoord_dict[node_Dyna] = coord_tuple
                coordTOnodes_dict[coord_tuple] = node_num
                data.insert(0, node_num)
                listOfListData.append(data)


    if writeFile:
        with open(writeFile, "w") as f:
            writer = csv.writer(f)
            writer.writerows(listOfListData)
    
    return pd.DataFrame(listOfListData, columns=["Node_ID_obj", "Node_ID", "Coord1", "Coord2", "Coord3"]), nodesTOcoord_dict, coordTOnodes_dict, nodes_DynaToObj_dict, nodes_ObjToDyna_dict



def cluster_DBSCAN(defect_elem_dict, nodes_coord_dict):

    """
    create cluster for defective elements.

    Inputs:
        Defect_elem_dict: A dictionary contains element ID as key and the list of nodes as value
        nodes_coord_dict: A dictionary contains node ID as key and coordinates list of the node as value

    Output:
        df: A dataframe with column titles "Elem_ID", "node1", "node2", "node3", "node4" and "cluster".


    """
    
    df = pd.DataFrame.from_dict(defect_elem_dict, orient="index").reset_index()
    df.columns = ["Elem_ID", "Node1", "Node2", "Node3", "Node4"]
    x, y, z = [], [], []
    for index, row in df.iterrows():
        coord  = [sum(x) for x in zip(nodes_coord_dict[int(row["Node1"])], nodes_coord_dict[int(row["Node2"])], nodes_coord_dict[int(row["Node3"])], nodes_coord_dict[int(row["Node4"])])]
        x.append(coord[0]/4)
        y.append(coord[1]/4)
        z.append(coord[2]/4)
        
    sub_df = pd.DataFrame({"x":x,
                            "y":y,
                            "z":z})
    fitted_dbscan = DBSCAN(3,min_samples=2).fit(sub_df)
    df["cluster"] = fitted_dbscan.labels_.tolist()
    # df = df.drop(labels=["x", "y", "z"], axis=1)
    assert df.shape[0]==len(defect_elem_dict), "number of defective elements mismatch after clustering"
    return df


def textureMap(m):
    """
    inputs:
        m: array of size (m,2) m number of vertex, and pc1 and pc2 as column
    
    output:
        vt: array of same size as m. containing the texture mapping location for each vertex
            (each element value of m matrix)
    
    """

    mini = np.min(m, axis=0)
    maxi = np.max(m, axis=0)

    vt = np.zeros(m.shape)
    for i in range(m.shape[0]):
        vt[i,0] = (1/(maxi[0]-mini[0]))*(m[i,0]-mini[0])
        vt[i,1] = (1/(maxi[1]-mini[1]))*(m[i,1]-mini[1])
    print(np.max(vt,axis=0))

    return vt

def calulatePercent(maxi,mini,texRatio,texSize):
    lengths = maxi-mini
    pix_lengths = lengths*texRatio
    return pix_lengths/texSize
def UVscale(vt_full, percent):
    return vt_full*percent + (1-percent)/2

def textureMap1(m, texRatio = None, texSize = None,  UVpercent = (0.9,0.9)):
    """
    inputs:
        m: array of size (m,2) m number of vertex, and pc1 and pc2 as column
    
    output:
        vt: array of same size as m. containing the texture mapping location for each vertex
            (each element value of m matrix)
    
    """


    
    mini = np.min(m, axis=0)
    maxi = np.max(m, axis=0)
    if texRatio:
        UVpercent = calulatePercent(maxi, mini, texRatio, texSize)
    rangex, rangey = UVpercent
    print(UVpercent)
    print(mini, maxi)    
    # print(mini, "\n", maxi)
    vt = np.zeros(m.shape)
    for i in range(m.shape[0]):
        vt_full = (1/(maxi[0]-mini[0]))*(m[i,0]-mini[0])
        vt[i,0] = UVscale(vt_full, rangex)
        vt_full = (1/(maxi[1]-mini[1]))*(m[i,1]-mini[1])
        # assert min(vt_full)==0.0 and max(vt_full)==1.0, "texture mapping not betwwen 0 to 1 limit in column 1"
        vt[i,1] = UVscale(vt_full, rangey)
    print(np.max(vt, axis=0))
    return vt



def pca(X, plot=False):
    """
        Inputs:
            X: (m,3) vertex positions

        Outputs:
            ans:
    """
    vertices_center = np.mean(X, axis=0)
    X_demeand = X-vertices_center

    covariance_matrix = np.cov(X_demeand, rowvar=False)
    eigen_vals, eigen_vecs = np.linalg.eigh(covariance_matrix)
    idx_sorted = np.argsort(eigen_vals)
    idx_sorted_decreasing = idx_sorted[::-1]
    eigen_vals_sorted = eigen_vals[idx_sorted_decreasing]
    eigen_vecs_sorted = eigen_vecs[idx_sorted_decreasing]
    X_pca = np.matmul(eigen_vecs_sorted.T, X_demeand.T).T

    return X_pca, eigen_vecs

def pca2(X, plot=False):
    """
        Inputs:
            X: (m,3) vertex positions

        Outputs:
            ans:
    """
    vertices_center = np.mean(X, axis=0)
    # print(X.shape)
    # print(np.min(X, axis=0))
    # print(np.max(X, axis=0))
    X_demeand = X-vertices_center

    covariance_matrix = np.cov(X_demeand, rowvar=False)
    # print(covariance_matrix)
    eigen_vals, eigen_vecs = np.linalg.eigh(covariance_matrix)
    # print(eigen_vals)
    idx_sorted = np.argsort(eigen_vals)
    idx_sorted_decreasing = idx_sorted[::-1]
    eigen_vals_sorted = eigen_vals[idx_sorted_decreasing]
    eigen_vecs_sorted = eigen_vecs[idx_sorted_decreasing]
    eigen_vecs_sorted_inverse = np.linalg.inv(eigen_vecs_sorted)
    # print(eigen_vecs_sorted_inverse.shape)
    # print(eigen_vecs_sorted_inverse)
    X_pca = np.matmul(eigen_vecs_sorted_inverse.T, X_demeand.T).T

    return X_pca, eigen_vecs

def arow(x,y):
    if abs(x)>abs(y):
        if x<0:
            startPointX = -10
            startPointY = -10*y/x
        else:
            startPointX = 10
            startPointY = 10*y/x
    else:
        if y<0:
            startPointY = -10
            startPointX = 10*x/y
        else:
            startPointY = 10
            startPointX = 10*x/y
    end_pointX = -startPointX
    end_pointY = -startPointY
    c = abs(startPointX-end_pointX)
    d = abs(startPointY-end_pointY)
    return startPointX, startPointY, c, d
    

if __name__=="__main__":
    # Uncomment to test pca related functions ============================
    # np.random.seed(1)
    # x = np.random.randint(5,20,(10,2))
    # center_vertices = np.mean(x, axis=0)
    # X_demeaned = x-center_vertices


    # fig, ax = plt.subplots(3, figsize=(8,8))
    # ax[0].scatter(X_demeaned[:,0], X_demeaned[:,1], c="red")
    # for i in range(x.shape[0]):
    #     ax[0].annotate("point-"+str(i), (X_demeaned[i,0], X_demeaned[i,1]))
    # ans, eigen_vecs = pca(x)
    # _,eigen_vecs_rotated = pca(ans)
    # origin = np.array([[0,0],[0,0]])
    # print(eigen_vecs[0,0], eigen_vecs[1,0])
    # ax[0].quiver(*origin, eigen_vecs[:,0], eigen_vecs[:,1], color=["r"], scale=5)
    # ax[0].quiver(*origin, eigen_vecs_rotated[:,0], eigen_vecs_rotated[:,1], color=["g"], scale=5)
    # ax[0].scatter(ans[:,0], ans[:,1], c="green")

    # for i in range(ans.shape[0]):
    #     ax[0].annotate("point-"+str(i), (ans[i,0], ans[i,1]))
    # plt.xlim([-10,10])
    # plt.ylim([-10,10])
    # # fig.savefig("images/pca.png")




    
    # # fig2, ax2 = plt.subplots(figsize=(8,8))
    # ax[1].scatter(X_demeaned[:,0], X_demeaned[:,1], c="red")
    # for i in range(x.shape[0]):
    #     ax[1].annotate("point-"+str(i), (X_demeaned[i,0], X_demeaned[i,1]))
    # ans, eigen_vecs = pca2(x)
    # _,eigen_vecs_rotated = pca(ans)
    # ax[1].quiver(*origin, eigen_vecs_rotated[:,0], eigen_vecs_rotated[:,1], color=["g"], scale=5)
    # ax[1].quiver(*origin, eigen_vecs[:,0], eigen_vecs[:,1], color=["r"], scale = 5)

    # ax[1].scatter(ans[:,0], ans[:,1], c="green")

    # for i in range(ans.shape[0]):
    #     ax[1].annotate("point-"+str(i), (ans[i,0], ans[i,1]))
    # plt.xlim([-10,10])
    # plt.ylim([-10,10])


    # ax[2].scatter(X_demeaned[:,0], X_demeaned[:,1], c="red")
    # for i in range(x.shape[0]):
    #     ax[2].annotate("point-"+str(i), (X_demeaned[i,0], X_demeaned[i,1]))
    # pca_sk = PCA()
    # ans = pca_sk.fit_transform(X_demeaned)
    # _,eigen_vecs_rotated = pca(ans)
    # ax[2].quiver(*origin, eigen_vecs_rotated[:,0], eigen_vecs_rotated[:,1], color=["g"], scale=5)
    # ax[2].quiver(*origin, eigen_vecs[:,0], eigen_vecs[:,1], color=["r"], scale = 5)

    # ax[2].scatter(ans[:,0], ans[:,1], c="green")

    # for i in range(ans.shape[0]):
    #     ax[2].annotate("point-"+str(i), (ans[i,0], ans[i,1]))
    # plt.xlim([-10,10])
    # plt.ylim([-10,10])

    # plt.savefig("images/pca2.png")
    # ===========================================
    # uncoment to test calulatePercent function =================================
    # a = np.array([1,2])
    # b = np.array([3,5])
    # s = np.array([40,50])
    # ans = calulatePercent(b,a,10,s)
    # print(ans)
    # ===============================================
    # Uncomment to test cluster_DBSCAN function ======================
    # defect_nodes_set = set([5,134,234,334,4])
    # nodes_coord_dict = {134:[1,10,20], 234:[2,10,20], 334:[20,100,500], 4:[20,100,501], 5:[54,345,3445]}
    # for row in defect_nodes_set:
    #     coord  = [sum(x) for x in zip(nodes_coord_dict[row["node1"]], nodes_coord_dict[row["node2"]], nodes_coord_dict[row["node3"]], nodes_coord_dict[row["node4"]])]
    # df = cluster_DBSCAN(defect_nodes_set, nodes_coord_dict)
    # print(df)
    # ===========================================
    # Uncomment and coose correct file to test cleanStrainData, cleanCoordData, cleanElemData ===============================
    # fileToClean = "/home/sakuni/phd/objective2/python/python/strain4"
    # writeFile = "/home/sakuni/phd/objective2/python/python/strain4_csv.csv"
    # strainDF = cleanStrainData(fileToClean, writeFile=writeFile)
    # ===================================================
    # Uncomment to test checkDefect function ====================================
    # data = pd.read_csv("/home/sakuni/phd/objective2/python/python/strain4_csv.csv")
    # print(data.head())
    # writeFile = "/home/sakuni/phd/objective2/python/python/stage4_defect_elem.csv"
    # df = checkDefect(data, writeFile=writeFile)
    # ====================================================