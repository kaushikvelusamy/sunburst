# sunburst

**

## Prototype to improve the performance of the entire conversion while applying gain correction and pyfai integration using parsl framework.

**

  

### Step 1: Gain Correction

Input:

 - Single .tiff file that contains the data to do the gain correction
 - Multiple .tiff files that are the actual (RAW) data

Output:

 - Multiple .tiff files that are the corrected data. 
 - This is saved in a directory that you define

### Step 2: Integration using PyFAI

Input:

- Multiple .tiff files that are the corrected data from the output of step 1
- A .poni file. This is a calibration file

Output:

- An .xy file for each .tiff file in input (Saved in the save directory is the output in step 1) 
- A single .txt file containing all the data from the .xy files
  

a CBF file is not same as tiff files but go through similar process – less space than tiff.
( collecting 250 CBF files in a second)
First experiment : 15,000 tiff files that’s passed to the step 1
Time taken for 15K files : 80 mins approx.
Time expected for 75K files : ~7 hours.


### Steps to run

# one time setup
`module load conda`

`conda activate`

`python -m venv --system-site-packages /lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/pyenv/`

`source /lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/pyenv/bin/activate`

`pip install --upgrade pip`

`pip install parsl`

`pip install pyfai`

`pip install PyQt5` #should not be needed


Create the directory structure for input and output files

compound         = "cono32"

dataset          = "cono32_20v_2s_6_00001"  

directory_src    = "/lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/test_dir_samples/PETRA/"

ponifile         = directory_src + "geometryNiAl.poni"

import_directory = directory_src + "insitu/" + dataset + "/"

export_path      = directory_src + "integrated/" + compound + "/insitu/" + dataset



`python intergration_petra_insitu_v3.py 0` # To save the plot

`python intergration_petra_insitu_v3.py 1` # Just conversion -not saving the plot
