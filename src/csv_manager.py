import pandas
import logging

from src import global_parameters
from src import execution_log


def read_input_file():
    """Read a CSV input file
    """

    execution_log.info_log("Reading CSV input file...")


    instance_name = global_parameters.instance_name()

    data_frame = pandas.read_csv(instance_name)

    if (global_parameters.output_size() > len(data_frame)):
        execution_log.info_log(
            "Changed output size. Instance is smaller than the provided size."
        )
        global_parameters.set_parameter("output_size", len(data_frame))


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
    
    lat_column_name = global_parameters.lat_column_name()
    lon_column_name = global_parameters.lon_column_name()

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

    





