import requests
import json
import random
import time

from src import global_parameters


def request_dist_and_time_remote(x, y):
    # Avoids being blocked for sending too many requests to OSRM demo server
    time.sleep(random.randint(0,10))
    
    url = ""
    url += "http://router.project-osrm.org/route/v1/driving/"
    url += str(x[1]) + "," + str(x[0]) + ";" + str(y[1]) + "," + str(y[0])
    
    response = requests.get(url)
    data = json.loads(response.content)
    
    if (data["code"].upper() == "OK"):
        return (data["routes"][0]["distance"], data["routes"][0]["duration"])

    return (None, None)

def request_dist_and_time_local(x, y):
    time.sleep((random.randint(0,10)/1000.0))
    url = ""
    url += 'http://localhost:5000/route/v1/driving/'
    url += str(x[1]) + ',' + str(x[0]) + ';' + str(y[1]) + ',' + str(y[0])
    
    response = requests.get(url)
    data = json.loads(response.content)
    
    if (data["code"].upper() == "OK"):
        return (data["routes"][0]["distance"], data["routes"][0]["duration"])

    return (None, None)


def request_dist_and_time(x, y):
    parameters_names = global_parameters.get_global_parameters_names()
    par_local = parameters_names[15]
    calcuate_distance_local = global_parameters.get_parameter(par_local)

    if (calcuate_distance_local):
        return request_dist_and_time_local(x, y)
    
    return request_dist_and_time_remote(x, y)


