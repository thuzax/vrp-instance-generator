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
        "latitude_column_name",
        "longitude_column_name",
        "limits",
        "min_lat",
        "max_lat",
        "min_lon",
        "max_lon"
    )

    # Name of the input instance
    _dict_parameters["instance_name"] = None

    # Name of the latitude and longitude columns in the input file
    _dict_parameters["latitude_column_name"] = "lat"
    _dict_parameters["longitude_column_name"] = "lon"

    # True if it was specified a box to limit the input map
    _dict_parameters["limits"] = False
    
    # Different from None if it was specified the limitations for the map
    _dict_parameters["min_latitude"] = None
    _dict_parameters["max_latitude"] = None
    _dict_parameters["min_longitude"] = None
    _dict_parameters["max_longitude"] = None


def set_parameter(parameter_name, value):
    """Change the value of a parameter
    """

    if (parameter_name not in _dict_parameters.keys()):
        raise exceptions.GlobalParamNotFound()
    
    _dict_parameters[parameter_name] = value


def get_parameter(parameter_name):
    """Get the value of a parameter
    """
    if (parameter_name not in _dict_parameters.keys()):
        raise exceptions.GlobalParamNotFound()
    
    return _dict_parameters(parameter_name)

def get_parameters():
    """Get a dictionary with copies of all the parameters 
    """
    return copy.deepcopy(_dict_parameters)



def get_global_parameters_names():
    """Return the parameter names in the following order
    instance_name, 
    latitude_column_name, 
    longitude_column_name, 
    min_latitude,
    max_latitude,
    min_longitude,
    max_longitude 
    """
    return dict_keys
