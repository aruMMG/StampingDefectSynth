from utils import readLines, v_from_objLines, writeLines, f_from_objLines

def f_defect(lines):
    count=0
    f_list_p_min = []
    for line in lines:
        if line.startswith("usemtl"):
            count+=1

        elif count>1:
            data = line.replace("/", " ")
            data = data.split()
            if len(data)>7:
                f_list_p_min.append([int(data[1]), int(data[4]), int(data[7])])
            elif len(data)>4:
                f_list_p_min.append([int(data[1]), int(data[3]), int(data[5])])
            else:
                f_list_p_min.append([int(data[1]), int(data[2]), int(data[3])])
    return f_list_p_min

p_min_file = "visualise8.obj"
saveFile = "heatmap_visualise2.obj"
p_min_lines = readLines(p_min_file)
v_list = v_from_objLines(p_min_lines)
v_list_str = []
for i in v_list:
    line = "v %.4f %.4f %.4f\n" % (i[0],i[1],i[2])
    v_list_str.append(line)
writeLines(saveFile, v_list_str)
del v_list_str


f_list_no_defect = []
f_list_p_min = []
count=0
for line in p_min_lines:
    if line.startswith("usemtl"):
        read=True
        count+=1
        continue

    if count==1:        
        data = line.replace("/", " ")
        data = data.split()
        if len(data)>7:
            f_list_no_defect.append([int(data[1]), int(data[4]), int(data[7])])
        elif len(data)>4:
            f_list_no_defect.append([int(data[1]), int(data[3]), int(data[5])])
        elif len(data)>2:
            f_list_no_defect.append([int(data[1]), int(data[2]), int(data[3])])
    elif count>1:
        data = line.replace("/", " ")
        data = data.split()
        if len(data)>7:
            f_list_p_min.append([int(data[1]), int(data[4]), int(data[7])])
        elif len(data)>4:
            f_list_p_min.append([int(data[1]), int(data[3]), int(data[5])])
        elif len(data)>2:
            f_list_p_min.append([int(data[1]), int(data[2]), int(data[3])])
f_list_no_defect_str = []
for i in f_list_no_defect:
    line = "f %d %d %d\n" % (i[0],i[1],i[2])
    f_list_no_defect_str.append(line)

f_list_p_min_str = []
for i in f_list_p_min:
    line = "f %d %d %d\n" % (i[0],i[1],i[2])
    f_list_p_min_str.append(line)
del f_list_no_defect

writeLines(saveFile, ["usemtl Default_OBJ\n"])
writeLines(saveFile, f_list_no_defect_str)
del f_list_no_defect_str
del v_list

outerfile = p_min_file
outerlines = p_min_lines
files = ["visualise105.obj", "visualise13.obj"]

outer_f_str = f_list_p_min_str
for file in files:
    f_current = []
    innerfile = file
    innerlines = readLines(innerfile)
    inner_f = f_defect(innerlines)
    inner_f_str = []
    for i in inner_f:
        line = "f %d %d %d\n" % (i[0],i[1],i[2])
        inner_f_str.append(line)
    del inner_f

    for line in outer_f_str:
        if line not in inner_f_str:
            f_current.append(line)
    writeLines(saveFile, f"usemtl {file}\n")
    writeLines(saveFile, f_current)
    outer_f_str = inner_f_str

writeLines(saveFile, f"usemtl checkFullCr5\n")
writeLines(saveFile, outer_f_str)