# sunburst

## A parsl prototype to improve the performance of the image conversion while applying gain correction with pyFAI


  
## Steps to run

## To create a parsl python environment from conda in polaris

`module load conda`

`conda activate`

`python -m venv /lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/parsl-pyenv/`

`source /lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/parsl-pyenv/bin/activate` [Add this path in the parsl config file]

`pip install requirements.txt` 


## To run the program

Just run python parsl_petra.py with the localthreads pilot or remote cpu or remote gpu configuration

For monitoring hub dont give run dir



## for the parallel parsl program

update the run_dir parameter in the parsl config file 

Just set your cpu or gpu config and run 

`cd sunburst/parsl_integration/parsl_petra.py`

`python parsl_petra.py`

To visualize parsl monitoring - follow https://parsl.readthedocs.io/en/stable/userguide/monitoring.html#visualization 

`parsl-visualize --debug`

you need the monitoring.db file generated automatically in runinfo dir 

enable port forwarding  ssh -L 50000:127.0.0.1:8080 username@polaris.alcf.anl.gov

and open 127.0.0.1:50000 in browser 




## Directory setup for the orignal the serial program

Create the directory structure for input and output files

compound         = "cono32"

dataset          = "cono32_20v_2s_6_00001"  

directory_src    = "/lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/test_dir_samples/PETRA/"

ponifile         = directory_src + "geometryNiAl.poni"

import_directory = directory_src + "insitu/" + dataset + "/"

export_path      = directory_src + "integrated/" + compound + "/insitu/" + dataset
