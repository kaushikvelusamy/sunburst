import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pyFAI
import fabio
import numpy as np
import matplotlib.pyplot as plt
import glob as glob
import os
import pyFAI
import fabio

from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pyFAI.calibrant import CALIBRANT_FACTORY
from pyFAI.goniometer import SingleGeometry
from skimage.io import imread
from PIL import Image
from tqdm import tqdm

mpl.use('Qt5Agg')



compound         = "cono32"
#dataset         = "cuno32_20v_2s_4_00002"
#dataset         = "feno33_1_26v_2s_1_00001"
dataset          = "cono32_20v_2s_6_00001"

directory_src    = "E:/Tyra/PETRA/"
import_directory = directory_src + "insitu/" + dataset + "/"
export_path      = directory_src + "integrated/" + compound + "/insitu/" + dataset
export_directory = export_path + "/"
savexy           = dataset + "_"
savetxt          = dataset + "_0_30000"

# savefigdir    = export_directory + "waterfall.png"

ponifile        = directory_src + "integrated/standards/lab6_1600mm_00001_fixedrot.poni"
numbins         = 1475
# spacing       = 20

if not os.path.exists(export_path):
    os.mkdir(export_path)                               # Create export folder if it doesn't exist


def get_image_series(opendir=import_directory, list_all=False, start_ind=0, end_ind=30000):
    get_images = sorted(glob.glob(opendir +"*.cbf"))    #genarates list of .tifs in import_directory
    if list_all:
        image_list = get_images                         # list all files in the directory
    else:
        image_list = get_images[start_ind:end_ind]
    return image_list


def do_integration(ponifile, numbins , savedir, savexy, savetxt, txtfile=True):
    ai       = pyFAI.load(ponifile)                     # Loads the calibration file
    pilatus  = pyFAI.detector_factory('PilatusCdTe2M')  # Loads pilatus information for calibration
    new_mask = pilatus.mask                             # Loads mask for detector gaps
    new_mask[870:1023, 847:900]     = 1                 # masks beamstop
    new_mask[870:1043, 900:985]     = 1
    new_mask[905:1090, 988:1060]    = 1
    new_mask[920:1100, 1060:1155]   = 1
    new_mask[955:1113, 1155:1230]   = 1
    new_mask[979:1140, 1230:1345]   = 1
    new_mask[1000:1160, 1345:1390]  = 1
    new_mask[1010:1175, 1390:1475]  = 1
    new_mask[1666:1675, 200:209]    = 1                 # masks bad pixels
    offset = 0
    
    all_images  = get_image_series()                    #list of .tif to integrate
    
    if txtfile:
        for images_num in tqdm(range(len(all_images))):
            one_image = all_images[images_num]                  # returns each filename.tif
            image_ind = str(one_image[-9:-4])                   # returns the sequence number of the file
            fimg      = fabio.open(one_image)                   # opens .tif file
            dest      = savedir + savexy + image_ind + ".xy"    # where integrated data will be stored
            res       = ai.integrate1d(fimg.data, numbins, unit="2th_deg", mask=new_mask, filename=dest)         # Integrates data and saves .xy file
    else:
        fig           = plt.figure(1, figsize=(11, 9.5))
        ax            = fig.add_subplot(111)
        
        for images_num in tqdm(range(len(all_images))):
            one_image = all_images[images_num]               # returns each filename.tif
            image_ind = str(one_image[-9:-4])                # returns the sequence number of the file
            fimg      = fabio.open(one_image)                # opens .tif file
            dest      = savedir + savexy + image_ind + ".xy" # where integrated data will be stored
            res       = ai.integrate1d(fimg.data, numbins, unit="2th_deg", mask=new_mask, filename=dest)         # Integrates data and saves .xy file
            
            for i in range(len(res[1])):
                res[1][i] += offset
            ax.plot(res[0], res[1], label = image_ind)
            offset  += spacing

        ax.set_xlim([0.0, 7.0])
        plt.xticks(ticks = (1,2,3,4,5,6,7), labels=(1,2,3,4,5,6,7), minor=True)
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.tick_params(which='both', bottom=True, top=False, left=True, right=False)
        ax.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False)
        ax.tick_params(axis='both', which='major', direction='in', length=8, width=1.5, color='black')
        ax.tick_params(axis='both', which='minor', direction='in', length=4, width=1.5, color='black')
        plt.xlabel("2 Theta")
        plt.ylabel("Intensity")
        plt.title(dataset)
        plt.legend(loc="upper left")
        plt.show()
        plt.savefig(savedir+ "waterfall.png", pad_inches=0.1)




do_integration(ponifile, numbins, export_directory, savexy, savetxt, txtfile=True)


# question on savetxt, spacing, savefigdir, dataset