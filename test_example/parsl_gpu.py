import parsl
from parsl import python_app, bash_app

#from parsl.configs.local_threads import config
#from parsl_configs.config_local_threads import config
#from parsl_configs.config_local_threads_pilot import config
#from parsl_configs.config_polaris_cpu import config, user_opts
from parsl_configs.config_polaris_gpu import config, user_opts

parsl.set_stream_logger() # <-- log everything to stdout
print(parsl.__version__)

# Load config for polaris
parsl.load(config)

# Application that runs hello_device on each GPU tile
@bash_app
def hello_device(stdout='hello.stdout', stderr='hello.stderr'):
    return 'echo "Hello Polaris CUDA device "$CUDA_VISIBLE_DEVICES; which pip'

outputdir = "gpu_example_outputs/"
tasks = []
for i in range(4):
    tasks.append(hello_device(stdout=outputdir+f"hello_{i}.stdout",  stderr=outputdir+f"hello_{i}.stderr"))

for t in tasks:
    t.result()

print("Hello tasks completed")
