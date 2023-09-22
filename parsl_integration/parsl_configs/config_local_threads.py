from parsl.config import Config
from parsl.executors.threads import ThreadPoolExecutor
from parsl.providers import LocalProvider


# Adjust your user-specific options here:
run_dir =   "/lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/parsl_integration"

user_opts = {
    "worker_init"  : f"source /lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/parsl-pyenv/bin/activate; cd {run_dir}", # load the environment where parsl is installed
}

config = Config( executors=[ ThreadPoolExecutor(  max_threads = 8, 
                                                  label       = 'local_threads',
                                                  #provider    = LocalProvider(worker_init = user_opts["worker_init"] )
                                                )
                           ],
                  run_dir          = run_dir
               )
