# Scripts adapted from Parsl docs
# https://parsl.readthedocs.io/en/stable/1-parsl-introduction.html

import parsl
from parsl import python_app 

#from parsl.configs.local_threads import config
#from parsl_configs.config_local_threads import config
from parsl_configs.config_local_threads_pilot import config
# from parsl_configs.config_polaris_cpu import config, user_opts
#from parsl_configs.config_polaris_gpu import config, user_opts

#parsl.set_stream_logger() # <-- log everything to stdout
print(parsl.__version__)

parsl.load(config)

# App that generates a random number after a delay
@python_app
def generate(limit,delay):
    from random import randint
    import time
    import pyFAI
    time.sleep(delay)
    return randint(1,limit)

# Generate 5 random numbers between 1 and 10
tasks = []
for i in range(16):
    tasks.append(generate(10,i))

# Wait for all apps to finish and collect the results
outputs = [t.result() for t in tasks]

# Print results
print(outputs)