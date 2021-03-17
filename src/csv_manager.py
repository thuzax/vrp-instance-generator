import pandas

from src import global_parameters
from src import execution_log


def read_input_file():
    """Read a CSV input file
    """

    execution_log.info_log("Reading CSV input file...")


    par_input_instance = global_parameters.get_global_parameters_names()[0]

    dict_globals = global_parameters.get_parameters()

    data_frame = pandas.read_csv(dict_globals[par_input_instance])

    execution_log.info_log("File read.")


    return data_frame

def write_output_file(data, output_name):
    """Write the data in a CSV file
    """

    execution_log.info_log("Writeing CSV file...")

    data.to_csv(output_name, index=False)

    execution_log.info_log("Done.")



def get_points_coordinates(data):
    """Get the latitude and longitude of all rows
    """
    parameters = global_parameters.get_global_parameters_names()
    lat_column_name = global_parameters.get_parameter(parameters[1])
    lon_column_name = global_parameters.get_parameter(parameters[2])

    points_list = []

    for ind, row in data.iterrows():
        latitude = row[lat_column_name]
        longitude = row[lon_column_name]

        point = (
            float(latitude), 
            float(longitude)
        )

        points_list.append(point)
    
    return points_list

    





