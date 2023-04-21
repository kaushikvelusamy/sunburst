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