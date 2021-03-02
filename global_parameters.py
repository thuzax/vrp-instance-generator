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
        "longitude_column_name"
    )

    _dict_parameters["instance_name"] = None

    _dict_parameters["latitude_column_name"] = "lat"

    _dict_parameters["longitude_column_name"] = "lon"

def set_parameter(parameter_name, value):
    """Change the value of a parameter
    """
    print(parameter_name)
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
    instance_name, latitude_column_name, longitude_column_name
    """
    return dict_keys
