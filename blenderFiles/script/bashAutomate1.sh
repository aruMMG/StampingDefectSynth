#!/bin/bash
j=1
csv_path=/home/aru/run6/40/renderImg/renderData/
for i in {1..1}
    do
        for filename in /home/aru/run6/40/objfile/1/*.obj
            do
                obj_name=$(basename "$filename" .obj)
                texname=$(find "/home/aru/run6/40/texture/1" -type f -print0 | shuf -z -n 1 )
                base_name=$(basename "$texname" .png)                        
                imgname=/home/aru/run6/40/renderImg/img_${obj_name}_${base_name}
                ((j=j+1))
                # echo $imgname
                # python checkbash.py $filename $texname $imgname
                blender --python /home/aru/run6/40/script/argument_multi_geometry1.py -- $filename $texname $imgname $csv_path
            done
    done
