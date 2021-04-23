import math
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
        "output_path",
        "distances_locally",
        "max_distance_pd",
        "generate_time_windows",
        "time_windows_horizon",
        "time_windows_size",
        "time_windows_size_max_variation",
        "generate_service_time",
        "min_service_time",
        "max_service_time",
        "generate_urb_rur_aptitude",
        "number_urban_centers",
        "max_urban_distance",
        "generation_urb_rur_method",
        "random_seed",
        "osrm_routed_path",
        "filo_path",
        "osrm_map_path",
        "config_file",
        "paths_file"
    )

    global _int_parameters
    _int_parameters = {
        "output_size",
        "generate_time_windows",
        "time_windows_horizon",
        "time_windows_size",
        "time_windows_size_max_variation",
        "number_urban_centers",
        "random_seed"
    }

    global _float_parameters
    _float_parameters = {
        "min_lat",
        "max_lat",
        "min_lon",
        "max_lon",
        "max_distance_pd",
        "max_urban_distance"
    }

    # Name of the input instance
    _dict_parameters["instance_name"] = None
    # Name of the output file
    _dict_parameters["output_name"] = None
    # Path to the output file
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

    # Max radius for the pickup and delivery generation limited by distance
    _dict_parameters["max_distance_pd"] = 10000000

    # Paramters for time windows
    _dict_parameters["generate_time_windows"] = False
    _dict_parameters["time_windows_horizon"] = 0
    _dict_parameters["time_windows_size"] = 0
    _dict_parameters["time_windows_size_max_variation"] = 0

    # Parameters for service time
    _dict_parameters["generate_service_time"] = False
    _dict_parameters["min_service_time"] = 0
    _dict_parameters["max_service_time"] = 0

    # Parameters for urban/rural aptitude
    _dict_parameters["generate_urb_rur_aptitude"] = False
    _dict_parameters["number_urban_centers"] = 0
    _dict_parameters["max_urban_distance"] = 0
    _dict_parameters["generation_urb_rur_method"] = None

    # File with the paths for external programs
    _dict_parameters["paths_file"] = "paths.json"

    # Path to osrm-routed command line
    _dict_parameters["osrm_routed_path"] = None

    # Path to osrm region that will be utilized
    _dict_parameters["osrm_map_path"] = None

    # Path to filo command line
    _dict_parameters["filo_path"] = None

    _dict_parameters["random_seed"] = 0




def set_parameter(parameter_name, value):
    """Change the value of a parameter
    """

    if (parameter_name == "per_number_urban_centers"):
        _dict_parameters["number_urban_centers"] = math.ceil(
                                    (value * _dict_parameters["output_size"]) 
                                    / 100
                                )
        return

    if (parameter_name not in _dict_parameters.keys()):
        raise exceptions.GlobalParamNotFound(parameter_name)
    
    if (parameter_name in _int_parameters and value is not None):
        value = int(value)

    if (parameter_name in _float_parameters and value is not None):
        value = float(value)

    if (parameter_name == "output_name"):
        splitted_path = value.split("/")
        name = splitted_path[-1]
        name = name.split(".")[0]

        _dict_parameters["output_path"] = "/".join(splitted_path[:-1])
        _dict_parameters["output_name"] = name

        return

    _dict_parameters[parameter_name] = value

    if (parameter_name == "generate_time_windows"
        and _dict_parameters["generate_time_windows"]
    ):
            _dict_parameters["generate_service_time"] = True


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
def output_path():
    return get_parameter("output_path")
def distances_locally():
    return get_parameter("distances_locally")
def max_distance_pd():
    return get_parameter("max_distance_pd")
def generate_time_windows():
    return get_parameter("generate_time_windows")
def time_windows_horizon():
    return get_parameter("time_windows_horizon")
def time_windows_size():
    return get_parameter("time_windows_size")
def time_windows_size_max_variation():
    return get_parameter("time_windows_size_max_variation")
def generate_service_time():
    return get_parameter("generate_service_time")
def min_service_time():
    return get_parameter("min_service_time")
def max_service_time():
    return get_parameter("max_service_time")
def filo_path():
    return get_parameter("filo_path")
def generate_urb_rur_aptitude():
    return _dict_parameters["generate_urb_rur_aptitude"]
def number_urban_centers():
    return _dict_parameters["number_urban_centers"]
def max_urban_distance():
    return _dict_parameters["max_urban_distance"]
def generation_urb_rur_method():
    return _dict_parameters["generation_urb_rur_method"]
def random_seed():
    return get_parameter("random_seed")
def osrm_routed_path():
    return get_parameter("osrm_routed_path")
def osrm_map_path():
    return get_parameter("osrm_map_path")
def paths_file():
    return get_parameter("paths_file")
def config_file():
    return get_parameter("config_file")
