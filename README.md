# Generating Synthetic Training Images to Detect Split Defects in Stamped Components
(https://ieeexplore.ieee.org/document/10317079)
## Implementation Details

This repository contains the implementation of a multi-stage approach for detecting rare defects, specifically necks and splits in sheet metal stamping. The process is outlined in four stages, with this repository providing the code for stages two and three, responsible for generating synthetic images.

### Stages:

1. **Data Preparation:**
   - Generate three text files (elem.txt, strain.txt, coord.txt) from finite element simulation (FEM).
  
2. **3D Object Generation:**
   - Utilize the data from stage one (A single FEM simulation) to create .obj files with plausible defect locations and random texture maps. The implementation for this stage is available in the 'CreateObj' folder.

3. **Synthetic Image Generation:**
   - Use the generated .obj files from stage two along with details in the 'Blender' folder to produce synthetic images.

4. **Defect Detection (Future Repository):**
   - A separate repository will be created for defect detection, using the synthetic images generated in stages two and three.


### Pipeline: Physical to 3D Defect Models

![Pipeline A](asset/pipelineA.jpg)

*Illustrates the steps of physically principled models and defect location generation: (i) Creating CAD models and arranging for stamping simulation, (ii) FEM simulation, and (iii) FLC-based algorithm used to generate 3D models with diverse yet random defect locations.*

### Pipeline: Synthetic Image Generation

![Pipeline B](asset/pipelineB.jpg)

*Illustrates the computer graphics-based synthetic image generation: models from stage 1 (left), texture coordinate mapping (middle), and final synthetic image (right).*

### Real vs Synthetic Image Comparison

![Results](asset/result.jpg)

*Shows a minor domain difference between real images (row 1) and synthetic images (row 2).*

