from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.providers import LocalProvider
from parsl.channels import LocalChannel
from parsl.monitoring.monitoring import MonitoringHub
from parsl.addresses import address_by_interface

# Adjust your user-specific options here:
#run_dir =   "/lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/test_example"

user_opts = {
    "worker_init"  : f"source /lus/grand/projects/datascience/kaushikv/parsl-aps/sunburst/parsl-pyenv/bin/activate; ", # load the environment where parsl is installed
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
                 #run_dir  = run_dir,
                 monitoring  =  MonitoringHub(  hub_address =   address_by_interface("bond0"),
                                hub_port                    =   55055,
                                monitoring_debug            =   True,
                                resource_monitoring_interval=   10,
                            )
                )
