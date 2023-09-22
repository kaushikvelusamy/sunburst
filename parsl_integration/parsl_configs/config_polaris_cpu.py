from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_interface
from parsl.providers import PBSProProvider
from parsl.launchers import MpiExecLauncher, GnuParallelLauncher
 

num_nodes = 1

# Adjust your user-specific options here:
run_dir =   "/lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/parsl_integration"

user_opts = {
    "worker_init"           : f"source /lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/parsl-pyenv/bin/activate; cd {run_dir}", # load the environment where parsl is installed
    "scheduler_options"     : "#PBS -l filesystems=home:grand" ,                             # specify any PBS options here, like filesystems
    "account"               : "datascience",
    "queue"                 : "debug-scaling",
    "walltime"              : "0:15:00",
    "nodes_per_block"       : num_nodes,                # think of a block as one job on polaris, so to run on the main queues, set this >= 10
    "cpus_per_node"         : 32,                       # Up to 64 with multithreading
    #"available_accelerators": 4,                        # Each Polaris node has 4 GPUs, setting this ensures one worker per GPU
    "cores_per_worker"      : 8,                        # this will set the number of cpu hardware threads per worker.  
}

#checkpoints = get_all_checkpoints(run_dir)
#print("Found the following checkpoints: ", checkpoints)
config = Config(
                    executors       =   [ HighThroughputExecutor(
                                                label                   =   "htex",
                                                heartbeat_period        =   15,
                                                heartbeat_threshold     =   120,
                                                worker_debug            =   True,
                                                #available_accelerators  =   user_opts["available_accelerators"], # if this is set, it will override other settings for max_workers if set
                                                cores_per_worker        =   user_opts["cores_per_worker"],
                                                address                 =   address_by_interface("bond0"),
                                                cpu_affinity            =   "alternating",      # Prevents thread contention
                                                prefetch_capacity       =   0,                  # Increase if you have many more tasks than workers
                                                start_method            =   "spawn",            # Needed to avoid interactions between MPI and os.fork
                                                provider                =   PBSProProvider (launcher        =   MpiExecLauncher(bind_cmd = "--cpu-bind", 
                                                                                                                                overrides= "--depth=64 --ppn 1"
                                                                                                                               ),# Ensures 1 manger per node and allows it to divide work to all 64 cores
                                                                                            account         =   user_opts["account"],
                                                                                            queue           =   user_opts["queue"],
                                                                                            scheduler_options = user_opts["scheduler_options"],  # PBS directives (header lines): for array jobs pass '-J' option
                                                                                            worker_init     =   user_opts["worker_init"],
                                                                                            nodes_per_block =   user_opts["nodes_per_block"],
                                                                                            cpus_per_node   =   user_opts["cpus_per_node"],
                                                                                            walltime        =   user_opts["walltime"],
                                                                                            #select_options  =   "ngpus=4",
                                                                                            init_blocks     =   1,
                                                                                            min_blocks      =   0,
                                                                                            max_blocks      =   1,      # Can increase more to have more parallel jobs
                                                                                            ),
                                                                ),
                                            ],
                    run_dir          = run_dir,
                    retries          = 2,
                    app_cache        = False
)
