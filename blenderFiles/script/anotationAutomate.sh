#!/bin/bash
save_path="/home/aru/run6/40/renderImg/annotationImg/"
tex_path="/home/aru/run6/40/texture_annotation/"
obj_path="/home/aru/run6/40/objfile/"
for filename in /home/aru/run6/40/renderImg/renderData/*.csv
    do
        blender --python /home/aru/run6/40/script/anotation.py -- $filename $tex_path $save_path $obj_path
    done

# filename="/home/aru/phd/objective2/blender/blendFile/renderedImage/stamping100/normal/renderData/img_obj1_tex4_b.csv"
# blender --python /home/aru/phd/objective2/blender/blendFile/script/anotation.py -- $filename $tex_path $save_path $obj_path
