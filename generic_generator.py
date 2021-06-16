import random
import numpy

from src import global_parameters
from src import arguments_handler
from src import status_variables
from src import csv_manager
from src import filter_csv
from src import generation_manager
from src import vrp_files_manager
from src import osrm_manager
from src import filo_manager

from constraints import *

if __name__=="__main__":
    global_parameters.init()
    arguments_handler.parse_command_line_arguments()
    arguments_handler.read_configuration_file()
    arguments_handler.read_paths_file()
    arguments_handler.read_constraints_config_file()

    random.seed(global_parameters.random_seed())
    numpy.random.seed(global_parameters.random_seed())

    exception = None

    status_variables.init()
    
    for constraint_object in global_parameters.constraints_objects():
        print(constraint_object.__dict__)

        print(constraint_object.get_constraint())

    