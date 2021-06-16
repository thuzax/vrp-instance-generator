import os
import subprocess
import time

from src import execution_log
from src import global_parameters
from src import status_variables


def init_osrm_server():
    """Initialize a osrm server using the command osrm-routed. It will not start a new server if there is another one running.
    """
    osrm_command_path = global_parameters.osrm_routed_path()
    osrm_map_path = global_parameters.osrm_map_path()
    
    command = ""
    command += osrm_command_path + " "
    command += osrm_map_path + " "
    command += "--algorithm=MLD" + " "
    command += "--max-table-size=1000000" + " "
    command += "--ip=127.0.0.1" + " "
    command += "--port=6969" + " "
    command += "--mmap"

    server_process = status_variables.osrm_server_process()

    if (server_process != None):
        execution_log.info_log("Process not initiated. There is already a running osrm server.")

    # print()
    execution_log.info_log(
        "Starting OSRM server with command: \n    " + command
    )

    # The command below runs the server and shows output in the terminal
    # server_process = subprocess.Popen("exec " + command, shell=True)
    
    # The commands below runs the server and shows the output in a log file 
    # callend #osrm-server-log-file.txt
    server_log_file = open("#osrm_server_log_file.log", "w")
    server_process = subprocess.Popen(
        "exec " + command, 
        shell=True, 
        stdout=server_log_file
    )

    status_variables.set_osrm_server_process(server_process)

    execution_log.info_log("Done.")

def finish_osrm_server():
    """Stop a osrm server if one exists
    """
    server_process = status_variables.osrm_server_process()

    if (server_process == None):
        execution_log.info_log("There was no osrm server started.")
    
    server_process.terminate()
    
    server_process = None

    status_variables.unset_osrm_server_process()
