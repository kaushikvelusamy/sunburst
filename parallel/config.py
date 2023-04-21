from parsl.config import Config

# PBSPro is the right provider for polaris:
from parsl.providers import PBSProProvider
# The high throughput executor is for scaling to HPC systems:
from parsl.executors import HighThroughputExecutor
# Use the MPI launcher
from parsl.launchers import MpiExecLauncher

from parsl.addresses import address_by_hostname

run_dir="/home/kaushikvelusamy/github/sunburst/parallel"

num_nodes = 1
polaris_config = Config(
    executors=[
        HighThroughputExecutor(
            available_accelerators=4,  # Ensures one worker per accelerator
            address=address_by_hostname(),
            cpu_affinity="alternating",  # Prevents thread contention
            prefetch_capacity=0,  # Increase if you have many more tasks than workers
            start_method="spawn",  # Needed to avoid interactions between MPI and os.fork
            provider=PBSProProvider(
                account="datascience",
                queue="preemptable",
                worker_init="module load conda; source /home/kaushikvelusamy/polaris/env/bin/activate; cd "+run_dir,
                walltime="0:15:00",
                scheduler_options="#PBS -l filesystems=home:grand",  # Change if data on other filesystem
                launcher=MpiExecLauncher(
                    bind_cmd="--cpu-bind", overrides="--depth=64 --ppn 1"
                ),  # Ensures 1 manger per node and allows it to divide work to all 64 cores
                select_options="ngpus=4",
                nodes_per_block=num_nodes,
                min_blocks=0,
                max_blocks=1,
                cpus_per_node=64,
            ),
        ),
    ]
)
