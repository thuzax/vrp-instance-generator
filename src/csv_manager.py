import pandas
import random

from src import global_parameters
from src import execution_log


def read_input_file():
    """Read a CSV input file
    """

    execution_log.info_log("Reading File...")


    par_input_instance = global_parameters.get_global_parameters_names()[0]

    dict_globals = global_parameters.get_parameters()

    data_frame = pandas.read_csv(dict_globals[par_input_instance])

    execution_log.info_log("File read.")


    return data_frame

def write_output_file(data, output_name):
    data.to_csv(output_name, index=False)
    





