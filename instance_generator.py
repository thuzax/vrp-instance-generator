from src import global_parameters
from src import arguments_handler
from src import csv_manager
from src import filter_csv
from src import execution_log
from src import calculate_distances_osrm as calculates_distances

import requests
import json
import pandas

def calculate_matrix(data):
    pass



def draw_elements(data, output_size):
    if (len(data) < output_size):
        return data

    data = data.sample(n=output_size)

    return data

if __name__=="__main__":
    global_parameters.init()
    arguments_handler.parse_command_line_arguments()
    
    # read input
    data = csv_manager.read_input_file()
    
    # filter data
    data = filter_csv.filter_data(data)

    parameters = global_parameters.get_global_parameters_names()

    par_output_size = parameters[13]
    par_output_name = parameters[14]

    output_size = global_parameters.get_parameter(par_output_size)
    output_name = global_parameters.get_parameter(par_output_name)

    # choose the random address/points
    data = draw_elements(data, output_size)

    calculate_matrix(data)

    # write data
    csv_manager.write_output_file(data, output_name)
