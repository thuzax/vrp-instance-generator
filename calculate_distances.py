import requests
import json


def request_osrm_dist(x, y):
    url = 'http://router.project-osrm.org/route/v1/driving/'
    url = url + str(x[1]) + ',' + str(x[0]) + ';' + str(y[1]) + ',' + str(y[0])
    response = requests.get(url)
    data = json.loads(response.content)
    
    return data