# Scripts adapted from Parsl docs
# https://parsl.readthedocs.io/en/stable/1-parsl-introduction.html

import parsl
from parsl import python_app
from parsl.data_provider.files import File
import os

#from parsl.configs.local_threads import config
#from parsl_configs.config_local_threads import config
from parsl_configs.config_local_threads_pilot import config
#from parsl_configs.config_polaris_cpu import config, user_opts
#from parsl_configs.config_polaris_gpu import config, user_opts

parsl.set_stream_logger() # <-- log everything to stdout
print(parsl.__version__)

parsl.load(config)

directory_src    = "/lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/samples/PETRA/"
input_directory  = directory_src + "input/"
output_directory = directory_src + "output/"

parsl_infile    = File(os.path.join(input_directory, '1.tif'),)
parsl_outfile   = File(os.path.join(output_directory, '1.xy'),)


# App that generates a random number after a delay
@python_app
def aps_integration(input_directory, output_directory, inputs=[], outputs=[]):
#def aps_integration(input_directory, output_directory):

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



    ponifile    = input_directory + "geometryNiAl.poni"
    numbins     = 1475

    pyfai_ai    = pyFAI.load(ponifile)                          # Loads the calibration file
    
    pilatus     = pyFAI.detector_factory('PilatusCdTe2M')       # Loads pilatus information for calibration
    new_mask    = pilatus.mask                                  # Loads mask for detector gaps
    new_mask[870:1023,  847:900]    = 1                         # masks beamstop
    new_mask[870:1043,  900:985]    = 1
    new_mask[905:1090,  988:1060]   = 1
    new_mask[920:1100,  1060:1155]  = 1
    new_mask[955:1113,  1155:1230]  = 1
    new_mask[979:1140,  1230:1345]  = 1
    new_mask[1000:1160, 1345:1390]  = 1
    new_mask[1010:1175, 1390:1475]  = 1
    new_mask[1666:1675, 200:209]    = 1                             # masks bad pixels

    get_image       = glob.glob(inputs[0].filepath)                 # genarates list of .tifs in import_directory
    #get_image       = sorted(glob.glob(input_directory +"*.tif"))             # genarates list of .tifs in import_directory

    #return(get_image)
    one_image       = get_image[0]                # returns each filename.tif

    input_tiff_file = fabio.open(one_image)                         # opens .tif file

    output_xy_file  = outputs[0].filepath                           # where integrated data will be stored
    #output_xy_file  = output_directory + "_" + ".xy"    # where integrated data will be stored

    
    # Integrates data and saves .xy file
    res             = pyfai_ai.integrate1d(input_tiff_file.data, numbins, unit="2th_deg", mask=new_mask, filename=output_xy_file)  
    return(get_image)       


tasks = []
tasks.append(aps_integration(input_directory, output_directory, inputs =[parsl_infile], outputs=[parsl_outfile] ) )
#tasks.append(aps_integration(input_directory, output_directory) )
    

# Wait for all apps to finish and collect the results
outputs = [t.result() for t in tasks]

# Print results
print(outputs)