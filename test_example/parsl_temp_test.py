# Scripts adapted from Parsl docs
# https://parsl.readthedocs.io/en/stable/1-parsl-introduction.html

import parsl
from parsl import python_app
from parsl.data_provider.files import File

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

parsl_infile    = File(input_directory)
parsl_outfile   = File(output_directory)


# App that generates a random number after a delay
@python_app
def aps_integration(input_directory, inputs=[], outputs=[]):
    import pyFAI
    ponifile    = input_directory + "geometryNiAl.poni"
    return(ponifile)
 
tasks = []
tasks.append(aps_integration(input_directory, inputs =[parsl_infile], outputs=[parsl_outfile] ) )
    

# Wait for all apps to finish and collect the results
outputs = [t.result() for t in tasks]

# Print results
print(outputs)