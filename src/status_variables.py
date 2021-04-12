def init():
    global _dict_status_variables
    _dict_status_variables = {}


    global dict_keys
    dict_keys = (
        "osrm_server_process"
    )

    # Stores the pid of the runing osrm server
    _dict_status_variables["osrm_server_process"] = None


def set_osrm_server_process(process):
    """Store the process of the osrm server if there is no other stored.
    """
    if (_dict_status_variables["osrm_server_process"] is not None):
        return
    _dict_status_variables["osrm_server_process"] = process

def unset_osrm_server_process():
    """Free the osrm server process allowing the initialization of a new one
    """
    _dict_status_variables["osrm_server_process"] = None

def osrm_server_process():
    return _dict_status_variables["osrm_server_process"]
