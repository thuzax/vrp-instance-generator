import exceptions
import copy

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
        "output_name"
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

def get_parameters():
    """Get a dictionary with copies of all the parameters 
    """
    return copy.deepcopy(_dict_parameters)



def get_global_parameters_names():
    """Return the parameter names as foollows (format: "<index>. <param_name>")
    
    0. instance_name,
    1. lat_column_name,
    2. lon_column_name,
    3. number_column_name,
    4. street_column_name,
    5. min_lat,
    6. max_lat,
    7. min_lon,
    8. max_lon,
    9. block_point_repetition,
    10. block_no_number,
    11. block_no_street,
    12. reaching_filter
    13. output_size,
    14. output_name,
    """
    return dict_keys
