import pandas
import random

import global_parameters


def read_input_file():
    """Read a CSV input file
    """
    par_input_instance = global_parameters.get_global_parameters_names()[0]

    dict_globals = global_parameters.get_parameters()

    data_frame = pandas.read_csv(dict_globals[par_input_instance])

    return data_frame

def write_output_file(data, output_name):
    data.to_csv(output_name, index=False)
    





