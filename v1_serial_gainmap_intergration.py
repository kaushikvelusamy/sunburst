import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from PIL import Image
from tqdm import tqdm
import glob as glob
import os
import pyFAI
import fabio

## -------------------- stage 1: Gain map stuff starts here --------------------

# Input begin
# Filename of gain map
gainmap = 'sunburst/sample_calculated_gainmap.tif' # This is the first input for gain
# Export folder name
# Set to whatever you want to name the folder gain corrected images are saved to
export_directory = 'Gain_corrected' # This defines the directory where the output will be
# Get all filenames for .tif images in current directory
filenames = glob.glob('*.tif') # This is the second input for gain
# Input end

# Generate boolean mask for intermodule gaps (value of -1); uses first image in series of imported images
g_mask = np.ma.masked_equal(imread(filenames[1]), -1).mask
# Generate boolean mask for dead pixels (value of -2); uses first image in series of imported images
d_mask = np.ma.masked_equal(imread(filenames[1]), -2).mask

# Import gain map
gmap = imread(gainmap)

# Check to see if export directory exists
if not os.path.exists(export_directory):
    os.mkdir(export_directory)  # Create export folder if it doesn't exist


# Define function to apply gain correction
def gain_correction(data, gain_map, gap_mask=1, dead_mask=1):
    '''
    Applies a gain map to some input data
    Assumes input data and gain map are the same shape, gain map should be multiplied by image
    Intermodule gap and dead pixel masks should be boolean arrays with 'True' at masked positions
    Replaces intermodule gap pixel values with -1, dead pixel values with -2

    Input (data, gain_map, gap_mask, dead_mask)
    Returns (corrected data)
    '''

    corr = np.multiply(data, gain_map)  # Multiply data by gain map
    corr = np.nan_to_num(corr)  # Remove nans
    corr[corr > 10 ** 300] = 0  # Remove any very large positive values created by +inf
    corr[corr < -10 ** 300] = 0  # Remove any very small negative values created by -inf

    # Apply intermodule gap and dead pixel masks
    corr[gap_mask] = -1  # Intermodule gap masked with -1
    corr[dead_mask] = -2  # Dead pixels maskex with -2

    return corr


for i in tqdm(range(0, len(filenames))):
    # Check to make sure file being imported isn't the gain map
    if filenames[i] != gainmap:
        im = imread(filenames[i])  # Import image
        im_corr = gain_correction(im, gmap, g_mask, d_mask)  # Apply gain correction
        # imsave(export_directory+'/'+os.path.basename(filenames[i]), im_corr) # Save gain corrected image
        export_im = Image.fromarray(np.float32(im_corr), mode='F')  # Create float32 image
        export_im.save(export_directory + '/' + os.path.basename(filenames[i]))

# The output is going to be the same number of tif 


## -------------------- stage 1:Gain map stuff ends here --------------------


## -------------------- stage 2: Integration stage starts here ----------

# Input begin
#directory of corrected tiffs
raw_tiff_dir = "sunburst/Gain_corrected/sample_tif_NiAl8_pt003sec_*.tif" #input for integration stage which we received from gain stage. 
#calibration file
poni_file = "sunburst/sample_poni_geometryNiAl.poni" # second input needed for stage 2
#Directory to save 2D array
save_2d_array = "sunburst/Gain_corrected/xydataset.txt"
# Input end

## There are 2 types of output files. 
### First: .xy files 
### Second:  1 .txt file 

all_images = glob.glob(raw_tiff_dir)
#########Set up intergration#########
#Loads the calibration files
ai = pyFAI.load(poni_file)
#Loads pilatus information for calibration
pilatus = pyFAI.detector_factory('PilatusCdTe2M')
#Loads mask for detector gaps
mask = pilatus.mask
#adds dead pixels to mask
mask[1127,1161] =-1
mask[1505:1507,1370:1373] =-1
mask[733,437] =-1

###intialize list for integrated data
#xy_dataint = []
xy_array = np.empty((len(all_images), 2500, 3)) # initialising on numpy array
for images_num in tqdm(range(len(all_images))):
    #returns each filename.tif
    one_image = all_images[images_num]
    #returns the sequence number of the file
    image_ind = str(one_image[-9:-4])
    xy_array[images_num,:,0] = image_ind
    fimg = fabio.open(one_image)
    dest = os.path.splitext(one_image)[0] + ".xy"
    res = ai.integrate1d(fimg.data, 2500, unit="2th_deg",mask=mask, filename=dest) # This is where .xy file is created and saved
    xy_array[images_num,:,1] = res[0]
    xy_array[images_num,:,2] = res[1]

xy_data2d = np.reshape(xy_array, ((xy_array.shape[0]*xy_array.shape[1]), 3))
np.savetxt(save_2d_array, xy_data2d, delimiter=' ')

## -------------------- stage 2: Integration stage ends here --------------------
