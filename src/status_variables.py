def init():
    global _dict_status_variables
    _dict_status_variables = {}


    global dict_keys
    dict_keys = (
        "osrm_server_process"
    )

    # Stores the pid of the runing osrm server
    _dict_status_variables["osrm_server_process"] = None


def set_osrm_server_process(pid):
    if (_dict_status_variables["osrm_server_process"] is not None):
        return
    _dict_status_variables["osrm_server_process"] = pid

def unset_osrm_server_process():
    _dict_status_variables["osrm_server_process"] = None

def osrm_server_process():
    return _dict_status_variables["osrm_server_process"]
