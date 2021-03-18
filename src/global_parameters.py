import copy

from src import exceptions

def init():
    """
    Initialize Global Parameters
    """
    global _dict_parameters
    _dict_parameters = {}

    global dict_keys
    dict_keys = (
        "instance_name",
        "lat_column_name",
        "lon_column_name",
        "number_column_name",
        "street_column_name",
        "min_lat",
        "max_lat",
        "min_lon",
        "max_lon",
        "block_point_repetition",
        "block_no_number",
        "block_no_street",
        "reaching_filter",
        "output_size",
        "output_name",
        "distances_locally",
        "config_file"
    )

    global _int_parameters
    _int_parameters = {
        "output_size"
    }

    global _float_parameters
    _float_parameters = {
        "min_lat",
        "max_lat",
        "min_lon",
        "max_lon"
    }

    # Name of the input instance
    _dict_parameters["instance_name"] = None
    # Name of the output file
    _dict_parameters["output_name"] = None
    # Number of rows of the output
    _dict_parameters["output_size"] = None

    # Name of the latitude and longitude columns in the input file
    _dict_parameters["lat_column_name"] = ["lat"]
    _dict_parameters["lon_column_name"] = ["lon"]
    # Specifies the name of the column with the address number
    _dict_parameters["number_column_name"] = None
    # Specifies the name of the column with the address street
    _dict_parameters["street_column_name"] = None
    
    # Indicates limits to the map factible area
    _dict_parameters["min_lat"] = None
    _dict_parameters["max_lat"] = None
    _dict_parameters["min_lon"] = None
    _dict_parameters["max_lon"] = None

    # If true, prevents repetition of points
    _dict_parameters["block_point_repetition"] = False
    # If true, prevents addresses without numbers
    _dict_parameters["block_no_number"] = False
    # If true, prevents addresses without street names
    _dict_parameters["block_no_street"] = False
    # If true, remove a point that can't reach another random point
    _dict_parameters["reaching_filter"] = False

    # If true, calculate distance running OSRM locally
    _dict_parameters["distances_locally"] = True

    # Parameter configuration file
    _dict_parameters["config_file"] = None



def set_parameter(parameter_name, value):
    """Change the value of a parameter
    """

    if (parameter_name not in _dict_parameters.keys()):
        raise exceptions.GlobalParamNotFound(parameter_name)
    
    if (parameter_name in _int_parameters and value is not None):
        value = int(value)

    if (parameter_name in _float_parameters and value is not None):
        value = float(value)

    _dict_parameters[parameter_name] = value


def get_parameter(parameter_name):
    """Get the value of a parameter
    """
    if (parameter_name not in _dict_parameters.keys()):
        raise exceptions.GlobalParamNotFound(parameter_name)
    
    return _dict_parameters[parameter_name]


# Gets
def instance_name():
    return get_parameter("instance_name")
def lat_column_name():
    return get_parameter("lat_column_name")
def lon_column_name():
    return get_parameter("lon_column_name")
def number_column_name():
    return get_parameter("number_column_name")
def street_column_name():
    return get_parameter("street_column_name")
def min_lat():
    return get_parameter("min_lat")
def max_lat():
    return get_parameter("max_lat")
def min_lon():
    return get_parameter("min_lon")
def max_lon():
    return get_parameter("max_lon")
def block_point_repetition():
    return get_parameter("block_point_repetition")
def block_no_number():
    return get_parameter("block_no_number")
def block_no_street():
    return get_parameter("block_no_street")
def reaching_filter():
    return get_parameter("reaching_filter")
def output_size():
    return get_parameter("output_size")
def output_name():
    return get_parameter("output_name")
def distances_locally():
    return get_parameter("distances_locally")
def config_file():
    return get_parameter("config_file")