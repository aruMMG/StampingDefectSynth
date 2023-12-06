"""
Create multiple obj file corresponding to crack and no crack geometry
"""

def separateGeometry(FilePath, savePath):
    with open(filePath, "r") as f:
        lines = f.readlines()
        # obj for no defect file
        count = -1

        with open(savePath+"nodefect.obj", "w") as g:
            for line in lines:
                data = line.split()
                if data[0]=="v":
                    g.write(line)
                elif data[0]=="f" and count==0:
                    g.write(line)
                elif data[0]=="usemtl":
                    count+=1
        finish = True
        count=1
        defect = -1
        while True:
            with open(savePath+str(count)+".obj", "w") as g:
                for line in lines:
                    data = line.split()
                    if data[0]=="v":
                        g.write(line)
                    elif data[0]=="vt":
                        g.write(line)
                    elif data[0]=="usemtl":
                        defect+=1
                    elif data[0]=="f" and count==defect:
                        g.write(line)
                if count>defect:
                    break
                count+=1
                defect= -1
                    


if __name__=="__main__":
    filePath = "/home/aru/phd/objective2/blender/blendFile/python/python/python/python/createOBJ/objFile/obj1.obj"
    savePath = "/home/aru/phd/objective2/blender/blendFile/python/python/python/python/createOBJ/objFile/obj1"
    separateGeometry(filePath, savePath)