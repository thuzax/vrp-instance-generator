import os
import subprocess

from src import execution_log
from src import global_parameters

def run_filo(instance, output_path):
    """Run the filo algorithm. It uses the variable filo_path, provided by the paths file.
    """

    instance = os.path.abspath(instance)
    output_path = os.path.abspath(output_path)
    
    filo_path = global_parameters.filo_path()

    command = ""
    command += filo_path + " "
    command += instance + " "
    command += "--parser X" + " "
    command += "--outpath " + output_path + " "

    print()
    execution_log.info_log(
        "Starting filo with command: \n    " + command
    )

    # The command below runs the server and shows output in the terminal
    # filo_process = subprocess.Popen("exec " + command, shell=True)
    
    # The commands below runs the server and shows the output in a log file 
    # callend #osrm-server-log-file.txt
    filo_log = open("#filo_log_file.log", "w")
    filo_process = subprocess.Popen(
        "exec " + command, 
        shell=True, 
        stdout=filo_log
    )

    filo_process.wait()

    execution_log.info_log("Done.")