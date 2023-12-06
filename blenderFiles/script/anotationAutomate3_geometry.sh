#!/bin/bash
save_path="/home/aru/run6/120DoubleCrack/renderImg/annotationImg/"
tex_path="/home/aru/run6/120DoubleCrack/texture_big_annotation/"
tex_path2="/home/aru/run6/120DoubleCrack/texture_small_annotation/"
obj_path="/home/aru/run6/120DoubleCrack/objFile/"
for filename in /home/aru/run6/120DoubleCrack/renderImg/renderData/*.csv
    do
        blender --python /home/aru/run6/120DoubleCrack/script/anotation_3_geometry.py -- $filename $tex_path $tex_path2 $save_path $obj_path
    done

# filename="/home/aru/phd/objective2/blender/blendFile/renderedImage/stamping100/normal/renderData/img_obj1_tex4_b.csv"
# blender --python /home/aru/phd/objective2/blender/blendFile/script/anotation.py -- $filename $tex_path $save_path $obj_path
