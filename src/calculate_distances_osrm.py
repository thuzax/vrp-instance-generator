import requests
import json
import random
import time

from src import global_parameters
from src import exceptions


def request_dist_and_time_remote(x, y):
    """Make a /route request to OSRM demo server and return distance and time between two points
    """
    # Avoids being blocked for sending too many requests to OSRM demo server
    time.sleep(random.randint(0,10))
    
    url = ""
    url += "http://router.project-osrm.org/route/v1/driving/"
    url += str(x[1]) + "," + str(x[0]) + ";" + str(y[1]) + "," + str(y[0])
    
    response = requests.get(url)

    if (response.status_code != 200):
        raise exceptions.CouldNotReachTheRoutingServer(
                                url, 
                                response.status_code
                            )

    data = json.loads(response.content)
    
    if (data["code"].upper() == "OK"):
        return (data["routes"][0]["distance"], data["routes"][0]["duration"])

    return (None, None)

def request_dist_and_time_local(x, y):
    """Make a /route request to OSRM local server and return distance and time between two points
    """
    time.sleep((random.randint(0,10)/1000.0))
    url = ""
    url += "http://localhost:5000/route/v1/driving/"
    url += str(x[1]) + "," + str(x[0]) + ";" + str(y[1]) + "," + str(y[0])
    
    response = requests.get(url)

    if (response.status_code != 200):
        print(x, y)
        raise exceptions.CouldNotReachTheRoutingServer(
                                url, 
                                response.status_code
                            )

    data = json.loads(response.content)
    
    if (data["code"].upper() == "OK"):
        return (data["routes"][0]["distance"], data["routes"][0]["duration"])

    return (None, None)


def request_dist_and_time(x, y):
    """Make a /route request to OSRM server and return distance and time between two points. The request will be remote if --run-distances-remote parameter is set, and locally otherwise.
    """
    parameters_names = global_parameters.get_global_parameters_names()
    par_local = parameters_names[15]
    calcuate_distance_local = global_parameters.get_parameter(par_local)

    if (calcuate_distance_local):
        return request_dist_and_time_local(x, y)
    
    return request_dist_and_time_remote(x, y)


def request_dist_and_time_from_source_local(source_position, points):
    """Make a /table request to OSRM local server and return distance and time between from a source to a list of points.
    """

    url = ""
    url += "http://localhost:5000/table/v1/driving/"

    for i in range(len(points)-1):
        url += str(points[i][1]) + "," + str(points[i][0]) + ";"
    
    url += str(points[-1][1]) + "," + str(points[-1][0])
    url += "?"
    url += "sources=" + str(source_position)
    url += "&destinations="

    for i in range(len(points)-1):
        url += str(i) + ";"
    
    url += str(len(points)-1)
    
    response = requests.get(url)

    if (response.status_code != 200):
        raise exceptions.CouldNotReachTheRoutingServer(
                                url, 
                                response.status_code
                            )
                            

    data = json.loads(response.content)

    if (data["code"].upper() != "OK"):
        return (None, None)
        
    times = data["durations"][0]

    returned_points = data["destinations"]

    distances = []

    for point in returned_points:
        distances.append(point["distance"])

    distances[source_position] = 0
    times[source_position] = 0

    return (distances, times)

def request_dist_and_time_from_source_remote(source_position, points):
    """Make a /table request to OSRM remote server and return distance and time between from a source to a list of points.
    """

    url = ""
    url += "http://router.project-osrm.org/table/v1/driving/"

    for i in range(len(points)-1):
        url += str(points[i][1]) + "," + str(points[i][0]) + ";"
    
    url += str(points[-1][1]) + "," + str(points[-1][0])
    url += "?"
    url += "sources=" + str(source_position)
    url += "&destinations="

    for i in range(len(points)-1):
        url += str(i) + ";"

    url += str(len(points)-1)
    
    response = requests.get(url)

    if (response.status_code != 200):
        raise exceptions.CouldNotReachTheRoutingServer(
                                url, 
                                response.status_code
                            )

    print(response)
    data = json.loads(response.content)
    
    if (data["code"].upper() != "OK"):
        return (None, None)
        
    times = data["durations"][0]

    returned_points = data["destinations"]

    distances = []

    for point in returned_points:
        distances.append(point["distance"])

    distances[source_position] = 0
    times[source_position] = 0

    return (distances, times)

    

def request_dist_and_time_from_source(source_position, points):
    """Make a /table request to OSRM server and return distance and time between from a source to a list of points. The request will be remote if --run-distances-remote parameter is set, and locally otherwise.
    """
    parameters_names = global_parameters.get_global_parameters_names()
    par_local = parameters_names[15]
    calcuate_distance_local = global_parameters.get_parameter(par_local)

    if (calcuate_distance_local):
        return request_dist_and_time_from_source_local(source_position, points)

    return request_dist_and_time_from_source_remote(source_position, points)