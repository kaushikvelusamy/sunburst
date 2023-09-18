import os
import glob as glob
import parsl
from parsl import python_app
from parsl.data_provider.files import File                          # For transfering file paths to remote machines - refer parsl Files

#from parsl.configs.local_threads import config         
#from parsl_configs.config_local_threads import config
from parsl_configs.config_local_threads_pilot import config
#from parsl_configs.config_polaris_cpu import config, user_opts
#from parsl_configs.config_polaris_gpu import config, user_opts

#parsl.set_stream_logger() # <-- log everything to stdout
#print(parsl.__version__)
parsl.load(config)

directory_src    = "/lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/samples/PETRA/"
input_directory  = directory_src + "input/"
output_directory = directory_src + "output/"
path_to_ponifile = input_directory + "geometryNiAl.poni"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)                                                  # Create export folder if it doesn't exist

temp_input_filenames         = sorted(glob.glob(input_directory +"*.tif"))      # generates list of .tifs in import_directory
# print("Total number of input files is ", len(temp_input_filenames))
# print("Input file names are "          , temp_input_filenames)

temp_output_filenames        = temp_input_filenames.copy()                      # generate list of output file names based on input filenames
for i in range(len(temp_output_filenames)):
    temp_output_filenames[i] = temp_output_filenames[i].replace("input", "output")
    temp_output_filenames[i] = temp_output_filenames[i].replace("tif", "xy")

# print("Total number of output files is ", len(temp_output_filenames))
# print("Output file names are "          , temp_output_filenames)
 

#num_workers = (user_opts["cpus_per_node"] / user_opts["cores_per_worker"]) * user_opts["nodes_per_block"]
num_workers = 8
#print("Num of parallel workers used for this program",num_workers)


@python_app
def aps_integration(img_start_index, img_end_index, path_to_ponifile, inputs=[], outputs=[]):
    import os
    import sys
    import numpy as np
    import pyFAI
    import fabio
    import numpy as np
    import glob as glob

    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from pyFAI.calibrant import CALIBRANT_FACTORY
    from pyFAI.goniometer import SingleGeometry
    from skimage.io import imread
    from PIL import Image
    from tqdm import tqdm

    numbins     = 1475
    pyfai_ai    = pyFAI.load(path_to_ponifile)                          # Loads the calibration file
    pilatus     = pyFAI.detector_factory('PilatusCdTe2M')               # Loads pilatus information for calibration

    new_mask    = pilatus.mask                                          # Loads mask for detector gaps
    new_mask[870:1023,  847:900]    = 1                                 # masks beamstop
    new_mask[870:1043,  900:985]    = 1
    new_mask[905:1090,  988:1060]   = 1
    new_mask[920:1100,  1060:1155]  = 1
    new_mask[955:1113,  1155:1230]  = 1
    new_mask[979:1140,  1230:1345]  = 1
    new_mask[1000:1160, 1345:1390]  = 1
    new_mask[1010:1175, 1390:1475]  = 1
    new_mask[1666:1675, 200:209]    = 1                                 # masks bad pixels

    for images_num in range(int(img_start_index), int(img_end_index)):
        tqdm(inputs[images_num].filepath)  
        one_image       = inputs[images_num].filepath                   # returns each filename.tif
        input_tiff_file = fabio.open(one_image)                         # opens .tif file
        output_xy_file  = outputs[images_num].filepath                  # where integrated data will be stored
        
        # Integrates data and saves .xy file
        res             = pyfai_ai.integrate1d(input_tiff_file.data, numbins, unit="2th_deg", mask=new_mask, filename=output_xy_file)         





# Divide the number of images based on the number of parallel workers. Eg 2 images per worker
img_start_index =   0
chunk           =   len(temp_input_filenames) / num_workers
img_end_index   =   chunk

tasks = []
for i in range(num_workers):
    tasks.append(aps_integration(img_start_index, img_end_index, path_to_ponifile, 
                                 inputs =[File(j) for j in temp_input_filenames], 
                                 outputs=[File(k) for k in temp_output_filenames] ) )
    img_start_index =   img_end_index
    img_end_index  +=  chunk 

# Wait for all apps to finish and collect the results
outputs = [t.result() for t in tasks]

# Print results
print(outputs)
