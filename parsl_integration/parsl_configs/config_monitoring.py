from parsl.monitoring.monitoring import MonitoringHub
from parsl.addresses import address_by_interface
#from parsl.addresses import address_by_hostname


monitoring  =   MonitoringHub(  hub_address                 =   address_by_interface("bond0"),
                                hub_port                    =   55055,
                                monitoring_debug            =   False,
                                resource_monitoring_interval=   10,
                            )



from parsl.utils import get_all_checkpoints
checkpoints     =   get_all_checkpoints(run_dir)
print("Found the following checkpoints: ", checkpoints)

checkpoint_files = checkpoints,
run_dir          = run_dir,
checkpoint_mode  = 'task_exit',