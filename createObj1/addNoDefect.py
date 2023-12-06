import random
from unittest import result
import numpy as np
import pandas as pd

def removeNoDefect(coordArr, coordDF, noDefect_elem_dict, defect_elem_dict, one_cluster_df,coordTOnodes_dict, nodesTOcoord_dict, nodes_ObjToDyna_dict, cluster,min0,min1,min2,max0,max1,max2):
    coord_to_remove = []
    elem_to_remove_from_one_cluster = set()
    for idx, row in one_cluster_df.iterrows():
        nodes = tuple([int(row.iloc[i]) for i in range(1,5)])

        # assert tuple(defect_elem_dict[int(row.iloc[0])])==nodes, "Mismatch of defect nodes to one cluster data frame"
        for node in nodes:
            coord = list(nodesTOcoord_dict[node])
            if min0>coord[0] or coord[0]>max0 or min1>coord[1] or coord[1]>max1:
                coord_to_remove.append(coord)
                elem_to_remove_from_one_cluster.add(int(row.iloc[0]))


    for col in one_cluster_df.columns:
        print(col)
    for elem in elem_to_remove_from_one_cluster:
        ind = one_cluster_df[one_cluster_df["Elem_ID"]==elem].index
        one_cluster_df.drop(ind, inplace=True)
        noDefect_elem_dict[elem] = defect_elem_dict[elem]
        defect_elem_dict.pop(elem)
    idx_to_remove = []
    for i in range(coordArr.shape[0]):
        if list(coordArr[i,:]) in coord_to_remove:
            idx_to_remove.append(i)
    coordArr = np.delete(coordArr, idx_to_remove, axis=0)
                
    return coordArr, one_cluster_df, noDefect_elem_dict

def defectLimit40(coordArr, change_position = True, trying = False):
    min0,min1,min2 =  np.min(coordArr, axis=0)
    max0,max1,max2 =  np.max(coordArr, axis=0)
    print("important")
    print(np.min(coordArr, axis=0))
    print(np.max(coordArr, axis=0))
    if change_position:
        # lenX = np.random.normal(-4, scale=1)
        if random.random() < 1.1:
            moveX = np.random.uniform(0,30)
            moveY = np.random.uniform(20,25)
            lenY = np.random.uniform(25,35)
            lenX = np.random.normal(17, scale = 1)
        else:
            moveX = np.random.uniform(-10,10)
            moveY = 0
            lenY = np.random.uniform(0,0.5)
            lenY_neg = np.random.uniform(-0.5,0)
        min0 = min0 + moveX
        max0 = min0 + lenX # + lenX
        min1 = min1 + moveY # + lenY_neg
        max1 = min1 + lenY
    if trying:
        min0 = min0 + 40
        max0 = min0 +20
        min1 = min1 + 20
        max1 = min1 + 30
    return min0,min1,min2, max0,max1,max2

def defectLimit60(coordArr, change_position = True, trying=False):
    min0,min1,min2 =  np.min(coordArr, axis=0)
    max0,max1,max2 =  np.max(coordArr, axis=0)
    print("important")
    print(np.min(coordArr, axis=0))
    print(np.max(coordArr, axis=0))
    if change_position:
        # lenX = np.random.normal(-4, scale=1)
        if random.random() < 1.1:
            moveX = np.random.uniform(0,30)
            moveY = np.random.uniform(-20,-10)
            lenY = np.random.uniform(30,45)
            lenX = np.random.normal(17, scale = 1)
        else:
            moveX = np.random.uniform(0,40)
            moveY = 0
            lenY = np.random.uniform(-2.5,2.5)
            lenY_neg = np.random.uniform(-2.5,2.5)
        min0 = min0 + moveX
        max0 = min0 + lenX # + lenX
        min1 = min1 + moveY # + lenY_neg
        max1 = min1 + lenY
    if trying:
        min0 = min0 + 30
        max0 = min0 +20
        min1 = min1 -20
        max1 = min1 + 40
    return min0,min1,min2, max0,max1,max2

def defectLimit80(coordArr, change_position = True):
    min0,min1,min2 =  np.min(coordArr, axis=0)
    max0,max1,max2 =  np.max(coordArr, axis=0)
    print("important")
    print(np.min(coordArr, axis=0))
    print(np.max(coordArr, axis=0))
    if change_position:
        lenX = np.random.normal(scale=1.67)
        if random.random() < 0.5:
            moveX = np.random.uniform(10,40)
            moveY = np.random.uniform(-10,10)
            lenY = np.random.uniform(-2.5,2.5)
            lenY_neg = np.random.uniform(-2.5,2.5)
        else:
            moveX = np.random.uniform(10,40)
            moveY = 0
            lenY = np.random.uniform(-5,5)
            lenY_neg = np.random.uniform(-5,5)
    min0 = min0 + moveX
    max0 = max0 + moveX + lenX
    min1 = min1 + moveY + lenY_neg
    max1 = max1 + moveY + lenY
    return min0,min1,min2, max0,max1,max2
def two_crack(count=1):
    if count==1:
        lenX = np.random.normal(loc=3, scale=1)
        if random.random() < 0.5:
            moveX = np.random.uniform(-10,10)    #   Two Crack
            moveY = np.random.uniform(-5,5)    #   Two Crack
            lenY = np.random.uniform(10,20)
            lenY_neg = np.random.uniform(-20,-10)
        else:
            moveX = np.random.uniform(-10,10)    #   Two Crack
            moveY = 0
            lenY = np.random.uniform(15,20)
            lenY_neg = np.random.uniform(-15,-20)
    elif count==2:
        lenX = np.random.normal(loc=3, scale=1)
        if random.random() < 0.5:
            moveX = np.random.uniform(-10,10)    #   Two Crack
            moveY = np.random.uniform(-5,5)    #   Two Crack
            lenY = np.random.uniform(5,10)
            lenY_neg = np.random.uniform(-5, -10)
        else:
            moveX = np.random.uniform(-10,10)    #   Two Crack
            moveY = 0
            lenY = np.random.uniform(5,15)
            lenY_neg = np.random.uniform(-15,-5)
    return moveX, moveY, lenX, lenY, lenY_neg

def defectLimit120(coordArr, change_position = True, large=False, count = False):
    min0,min1,min2 =  np.min(coordArr, axis=0)
    max0,max1,max2 =  np.max(coordArr, axis=0)
    # print("important")
    # print(np.min(coordArr, axis=0))
    # print(np.max(coordArr, axis=0))
    if change_position:
        if count and not large:
            moveX, moveY, lenX, lenY, lenY_neg = two_crack(count=count)
        else:
            if large:
                lenX = np.random.normal(loc=3, scale=1)
                if random.random() < 1.5:
                    moveX = np.random.uniform(-5,10)   #   Original Run4
                    # moveX = np.random.uniform(-10,0)    #   Two Crack
                    moveY = np.random.uniform(-3,3)   #   Original Run4
                    # moveY = np.random.uniform(-5,5)    #   Two Crack
                    lenY = np.random.uniform(20, 25)
                    lenY_neg = np.random.uniform(-20,-25)
                else:
                    moveX = np.random.uniform(-5,10)   #   Original Run4
                    # moveX = np.random.uniform(-10,0)    #   Two Crack
                    moveY = 0
                    lenY = np.random.uniform(20, 25)
                    lenY_neg = np.random.uniform(-20, -25)
            else:
                lenX = np.clip(np.random.normal(scale=1.67), a_min=0, a_max=4)
                if random.random() < 0.5:
                    moveX = np.random.uniform(-10,20)   #   Original Run4
                    # moveX = np.random.uniform(-10,0)    #   Two Crack
                    moveY = np.random.uniform(-10,10)   #   Original Run4
                    # moveY = np.random.uniform(-5,5)    #   Two Crack
                    lenY = np.random.uniform(10,25)
                    lenY_neg = np.random.uniform(-25, -10)
                else:
                    moveX = np.random.uniform(-10,20)   #   Original Run4
                    # moveX = np.random.uniform(-10,0)    #   Two Crack
                    moveY = 0
                    lenY = np.random.uniform(10,25)
                    lenY_neg = np.random.uniform(-25,-10)
    min0 = min0 + moveX
    max0 = max0 + moveX + lenX
    min1 = min1 + moveY + lenY_neg
    max1 = max1 + moveY + lenY
    return min0,min1,min2, max0,max1,max2
def two_crack140(count=1):
    if count==1:
        lenX = np.random.normal(loc=3, scale=1)
        if random.random() < 0.5:
            moveX = np.random.uniform(-10,10)    #   Two Crack
            moveY = np.random.uniform(-5,5)    #   Two Crack
            lenY = np.random.uniform(10,20)
            lenY_neg = np.random.uniform(-20,-10)
        else:
            moveX = np.random.uniform(-10,10)    #   Two Crack
            moveY = 0
            lenY = np.random.uniform(15,20)
            lenY_neg = np.random.uniform(-15,-20)
    elif count==2:
        lenX = np.random.normal(loc=3, scale=1)
        if random.random() < 0.5:
            moveX = np.random.uniform(-10,10)    #   Two Crack
            moveY = np.random.uniform(-5,5)    #   Two Crack
            lenY = np.random.uniform(5,10)
            lenY_neg = np.random.uniform(-5, -10)
        else:
            moveX = np.random.uniform(-10,10)    #   Two Crack
            moveY = 0
            lenY = np.random.uniform(5,15)
            lenY_neg = np.random.uniform(-15,-5)
    return moveX, moveY, lenX, lenY, lenY_neg

def defectLimit140(coordArr, change_position = True, large=False, count = False):
    min0,min1,min2 =  np.min(coordArr, axis=0)
    max0,max1,max2 =  np.max(coordArr, axis=0)
    # print("important")
    # print(np.min(coordArr, axis=0))
    # print(np.max(coordArr, axis=0))
    if change_position:
        if count and not large:
            moveX, moveY, lenX, lenY, lenY_neg = two_crack140(count=count)
        else:
            if large:
                lenX = np.random.normal(loc=-12, scale=1)
                if random.random() < 1.5:
                    moveX = np.random.uniform(-5,10)   #   Original Run4
                    # moveX = np.random.uniform(-10,0)    #   Two Crack
                    moveY = np.random.uniform(-3,3)   #   Original Run4
                    # moveY = np.random.uniform(-5,5)    #   Two Crack
                    lenY = np.random.uniform(5, 10)
                    lenY_neg = np.random.uniform(-5,-10)
                else:
                    moveX = np.random.uniform(-5,10)   #   Original Run4
                    # moveX = np.random.uniform(-10,0)    #   Two Crack
                    moveY = 0
                    lenY = np.random.uniform(10, 15)
                    lenY_neg = np.random.uniform(-10, -15)
            else:
                lenX = np.clip(np.random.normal(scale=1.67), a_min=0, a_max=4)
                if random.random() < 0.5:
                    moveX = np.random.uniform(-10,20)   #   Original Run4
                    # moveX = np.random.uniform(-10,0)    #   Two Crack
                    moveY = np.random.uniform(-10,10)   #   Original Run4
                    # moveY = np.random.uniform(-5,5)    #   Two Crack
                    lenY = np.random.uniform(5,20)
                    lenY_neg = np.random.uniform(-20, -5)
                else:
                    moveX = np.random.uniform(-10,20)   #   Original Run4
                    # moveX = np.random.uniform(-10,0)    #   Two Crack
                    moveY = 0
                    lenY = np.random.uniform(5,20)
                    lenY_neg = np.random.uniform(-20,-5)
    min0 = min0 + moveX
    max0 = max0 + moveX + lenX
    min1 = min1 + moveY + lenY_neg
    max1 = max1 + moveY + lenY
    return min0,min1,min2, max0,max1,max2
def defectLimit170 (coordArr, change_position = True):
    min0,min1,min2 =  0,0,0 # np.min(coordArr, axis=0)
    max0,max1,max2 =  0,0,0 # np.max(coordArr, axis=0)
    print("important")
    # print(np.min(coordArr, axis=0))
    # print(np.max(coordArr, axis=0))
    if change_position:
        lenX = np.random.normal(25, scale=1.67)
        if random.random() < 1.1:
            moveX = np.random.uniform(-10,-20)
            moveY = np.random.uniform(-5,5)
            lenY = np.random.uniform(40,50)
            lenY_neg = np.random.uniform(-40,-50)
        else:
            moveX = np.random.uniform(-20,20)
            moveY = 0
            lenY = np.random.uniform(0,50)
            lenY_neg = np.random.uniform(-50,0)
    min0 = min0 + moveX
    max0 = max0 + moveX + lenX
    min1 = min1 + moveY + lenY_neg
    max1 = max1 + moveY + lenY
    return min0,min1,min2, max0,max1,max2
def defectLimitFullLength (coordArr, change_position = True):
    min0,min1,min2 =  0,0,0 # np.min(coordArr, axis=0)
    max0,max1,max2 =  0,0,0 # np.max(coordArr, axis=0)
    print("important")
    # print(np.min(coordArr, axis=0))
    # print(np.max(coordArr, axis=0))
    if change_position:
        lenY = np.random.normal(25, scale=1.67)
        if random.random() < 1.1:
            moveY = np.random.uniform(-10,0)
            moveX = np.random.uniform(-5,5)
            lenX = np.random.uniform(40,50)
            lenX_neg = np.random.uniform(-40,-50)
        else:
            moveX = np.random.uniform(-20,20)
            moveY = 0
            lenY = np.random.uniform(0,50)
            lenY_neg = np.random.uniform(-50,0)
    min0 = min0 + moveX + lenX_neg
    max0 = max0 + moveX + lenX
    min1 = min1 + moveY
    max1 = max1 + moveY + lenY
    return min0,min1,min2, max0,max1,max2

def addNoDefect(args, coordArr, coordDF, noDefect_elem_dict, defect_elem_dict, one_cluster_df, coordTOnodes_dict, nodesTOcoord_dict, nodes_ObjToDyna_dict, cluster, change_position = True, count=False):
    if args.fullDefect:
        min0,min1,min2, max0,max1,max2 =  defectLimitFullLength(coordArr, change_position)
    elif args.sample_size==40:
        min0,min1,min2, max0,max1,max2 =  defectLimit40(coordArr, change_position = True, trying = False)
    elif args.sample_size==60:
        min0,min1,min2, max0,max1,max2 =  defectLimit60(coordArr, change_position = True, trying=False)
    elif args.sample_size==80:
        min0,min1,min2, max0,max1,max2 =  defectLimit80(coordArr, change_position)
    elif args.sample_size==120:
        if args.double and count:
            min0,min1,min2, max0,max1,max2 =  defectLimit120(coordArr, change_position, count=count)
        else:
            min0,min1,min2, max0,max1,max2 =  defectLimit120(coordArr, change_position)
    elif args.sample_size==140:
        if args.double and count:
            min0,min1,min2, max0,max1,max2 =  defectLimit140(coordArr, change_position, count=count)
        else:
            min0,min1,min2, max0,max1,max2 =  defectLimit140(coordArr, change_position)
    elif args.sample_size==170:
        min0,min1,min2, max0,max1,max2 =  defectLimit170(coordArr, change_position)
    
    print(min0,min1,min2, max0,max1,max2)
    nodesInside = []
    for idx, row in coordDF.iterrows():
        # if min0<float(row["Coord1"])<max0 and min1<float(row["Coord2"])<max1 and min2<float(row["Coord3"])<max2:
        if min0<float(row["Coord1"])<max0 and min1<float(row["Coord2"])<max1:
            nodesInside.append(nodes_ObjToDyna_dict[int(row["Node_ID_obj"])])
            coordArr = np.vstack((coordArr, [float(row["Coord1"]),float(row["Coord2"]),float(row["Coord3"])]))

    df_list = []
    pop_key = []
    for key, val in noDefect_elem_dict.items():
        result = all(node in nodesInside for node in val)
        if result:
            # add element to one_cluster_df
            val.insert(0, key)
            val.insert(5, cluster)
            df_list.append(val)
            pop_key.append(key)
    df_columns = list(one_cluster_df.columns)
    df_tem = pd.DataFrame(df_list, columns=df_columns)
    one_cluster_df = one_cluster_df.append(df_tem, ignore_index=True)
    
    for key in pop_key:
        defect_elem_dict[key] = noDefect_elem_dict[key]
        noDefect_elem_dict.pop(key)
    if not args.sample_size==140:
        assert len(defect_elem_dict)==one_cluster_df.shape[0], "number of defective elements mismatch for single defect"
    coordArr, one_cluster_df, noDefect_elem_dict = removeNoDefect(coordArr, coordDF, noDefect_elem_dict, defect_elem_dict, one_cluster_df, coordTOnodes_dict, nodesTOcoord_dict, nodes_ObjToDyna_dict, cluster,min0,min1,min2,max0,max1,max2)    
    return coordArr, one_cluster_df, noDefect_elem_dict
