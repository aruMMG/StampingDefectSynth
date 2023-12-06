#!/bin/bash
j=1
csv_path=/home/aru/run6/120DoubleCrack/renderImg/renderData/
for i in {1..1}
    do
        for filename in /home/aru/run6/120DoubleCrack/objFile/1/*.obj
            do
                obj_name=$(basename "$filename" .obj)
                texname=$(find "/home/aru/run6/120DoubleCrack/texture/big/1" -type f -print0 | shuf -z -n 1 )
                texname2=$(find "/home/aru/run6/120DoubleCrack/texture/small/1" -type f -print0 | shuf -z -n 1 )
                base_name=$(basename "$texname" .png)                        
                base_name2=$(basename "$texname2" .png)                        
                imgname=/home/aru/run6/120DoubleCrack/renderImg/img_${obj_name}_${base_name}_${base_name2}
                ((j=j+1))
                # echo $imgname
                # python checkbash.py $filename $texname $imgname
                blender --python /home/aru/run6/120DoubleCrack/script/argument_3_geometry.py -- $filename $texname $texname2 $imgname $csv_path
            done
    done
