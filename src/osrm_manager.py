import os
import subprocess
import time

from src import execution_log
from src import global_parameters
from src import status_variables


def init_osrm_server():

    osrm_command_path = global_parameters.osrm_routed_path()
    osrm_map_path = global_parameters.osrm_map_path()
    
    command = ""
    command += osrm_command_path + " "
    command += osrm_map_path + " "
    command += "--algorithm=MLD" + " "
    command += "--max-table-size=1000000"

    print()

    print(command)

    print()

    server_process = status_variables.osrm_server_process()

    if (server_process != None):
        execution_log.info_log("Process not initiated. There is already a running osrm server.")

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

    time.sleep(2)

def finish_osrm_server():
    server_process = status_variables.osrm_server_process()

    if (server_process == None):
        execution_log.info_log("There was no osrm server started.")
    
    server_process.kill()
    
    server_process = None

    status_variables.unset_osrm_server_process()
