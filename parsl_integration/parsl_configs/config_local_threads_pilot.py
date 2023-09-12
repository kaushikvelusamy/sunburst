from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.providers import LocalProvider
from parsl.channels import LocalChannel

# Adjust your user-specific options here:
run_dir =   "/lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/parsl_integration"

user_opts = {
    "worker_init"  : f"source /lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/pyenv/bin/activate; cd {run_dir}", # load the environment where parsl is installed
}

config = Config( executors=[ HighThroughputExecutor( label           = "htex_Local",
                                                     worker_debug    = True,
                                                     cores_per_worker= 1,
                                                     provider        = LocalProvider( channel     = LocalChannel(),
                                                                                      init_blocks = 1,
                                                                                      max_blocks  = 1,
                                                                                      worker_init = user_opts["worker_init"]
                                                                                    ),
                                                      )
                           ],
                 strategy = None,
                 run_dir  = run_dir
                )
