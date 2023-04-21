import parsl
from parsl import python_app
from parsl import bash_app
# Import config for polaris from config.py
from config import polaris_config

# Load config for polaris
parsl.load(polaris_config)

# Application that runs hello_device on each GPU tile
@bash_app
def hello_device(stdout='hello.stdout', stderr='hello.stderr'):
    return 'echo "Hello Polaris CUDA device "$CUDA_VISIBLE_DEVICES'

outputdir = "github/sunburst/parallel/outputs/"
tasks = []
for i in range(4):
    tasks.append(hello_device(stdout=outputdir+f"hello_{i}.stdout", 
                              stderr=outputdir+f"hello_{i}.stderr"))

for t in tasks:
    t.result()

print("Hello tasks completed")
