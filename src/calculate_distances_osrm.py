import requests
import json
import random
import time
import numpy
import math

from src import global_parameters
from src import exceptions
from src import execution_log


def send_request(url):
    total_time = 0
    has_response = False
    while (not has_response and total_time < 60):
        if (total_time > 0):
            execution_log.info_log("Retrying")
        try:
            response = requests.get(url)
            has_response = True
        except Exception:
            time.sleep(1)
            total_time += 1
    
    return response


def request_dist_and_time_remote(x, y):
    """Make a /route request to OSRM demo server and return distance and time between two points
    """
    # Avoids being blocked for sending too many requests to OSRM demo server
    time.sleep(random.randint(0,10))
    
    url = ""
    url += "http://router.project-osrm.org/route/v1/driving/"
    url += str(x[1]) + "," + str(x[0]) + ";" + str(y[1]) + "," + str(y[0])
    
    response = send_request(url)

    if (response.status_code != 200):
        raise exceptions.CouldNotReachTheRoutingServer(
                                url, 
                                response.status_code
                            )

    data = json.loads(response.content)
    
    if (data["code"].upper() == "OK"):
        distance = data["routes"][0]["distance"]
        travel_time = data["routes"][0]["duration"] / 60
        return (distance, travel_time)
    
    return (None, None)

def request_dist_and_time_local(x, y):
    """Make a /route request to OSRM local server and return distance and time between two points
    """
    time.sleep((random.randint(0,10)/1000.0))
    url = ""
    url += "http://127.0.0.1:6969/route/v1/driving/"
    url += str(x[1]) + "," + str(x[0]) + ";" + str(y[1]) + "," + str(y[0])

    response = send_request(url)

    if (response.status_code != 200):
        raise exceptions.CouldNotReachTheRoutingServer(
                                url, 
                                response.status_code
                            )

    data = json.loads(response.content)
    
    if (data["code"].upper() == "OK"):
        distance = data["routes"][0]["distance"]
        travel_time = data["routes"][0]["duration"] / 60
        return (distance, travel_time)

    return (None, None)


def request_dist_and_time(x, y):
    """Make a /route request to OSRM server and return distance and time between two points. The request will be remote if --run-distances-remote parameter is set, and locally otherwise.
    """
    calcuate_distance_local = global_parameters.distances_locally()

    if (calcuate_distance_local):
        return request_dist_and_time_local(x, y)
    
    return request_dist_and_time_remote(x, y)


def request_dist_and_time_from_source_local(source_position, points):
    """Make a /table request to OSRM local server and return distance and time between from a source to a list of points.
    """

    url = ""
    url += "http://127.0.0.1:6969/table/v1/driving/"

    for i in range(len(points)-1):
        url += str(points[i][1]) + "," + str(points[i][0]) + ";"
    
    url += str(points[-1][1]) + "," + str(points[-1][0])
    url += "?"
    url += "sources=" + str(source_position)
    url += "&destinations="

    for i in range(len(points)-1):
        url += str(i) + ";"
    
    url += str(len(points)-1)
    
    response = send_request(url)

    if (response.status_code != 200):
        raise exceptions.CouldNotReachTheRoutingServer(
                                url, 
                                response.status_code
                            )
                            

    data = json.loads(response.content)

    if (data["code"].upper() != "OK"):
        return (None, None)
        
    times = data["durations"][0]

    for i in range(len(times)):
        times[i] = times[i] / 60
        times[i] = math.ceil(times[i])

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
    
    response = send_request(url)

    if (response.status_code != 200):
        raise exceptions.CouldNotReachTheRoutingServer(
                                url, 
                                response.status_code
                            )

    data = json.loads(response.content)
    
    if (data["code"].upper() != "OK"):
        return (None, None)
        
    times = data["durations"][0]

    for i in range(len(times)):
        times[i] = times[i] / 60
        times[i] = math.ceil(times[i])

    returned_points = data["destinations"]

    distances = []

    for point in returned_points:
        distances.append(point["distance"])

    distances[source_position] = 0
    times[source_position] = 0

    distances = numpy.array(distances)
    times = numpy.array(times)

    return (distances, times)

    

def request_dist_and_time_from_source(source_position, points):
    """Make a /table request to OSRM server and return distance and time between from a source to a list of points. The request will be remote if --run-distances-remote parameter is set, and locally otherwise.
    """
    calcuate_distance_local = global_parameters.distances_locally()

    if (calcuate_distance_local):
        return request_dist_and_time_from_source_local(source_position, points)

    return request_dist_and_time_from_source_remote(source_position, points)