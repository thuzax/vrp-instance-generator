import subprocess
import requests
import json
import random
import time
import numpy
import math

from src import exceptions
from src import execution_log

from src.matrices_calculation import DistancesAndTimesCalculator

class DistancesAndTimesOSRM(DistancesAndTimesCalculator):
    # Acquired from configuration file
    distances_locally = True
    osrm_routed_command_location = None
    osrm_regions_map_files = None
    osrm_instance_region = None
    
    # Modified while running
    running_osrm = False
    server_process = None


    def __init__(self):
        super().__init__("Open Source Routing Machine")
        if (self.validate_osrm_inputs()):
            self.init_osrm_server()

    def __del__(self):
        self.finish_osrm_server()


    def validate_osrm_inputs(self):
        if (self.osrm_routed_command_location is None):
            return False
        if (self.osrm_regions_map_files is None):
            return False
        if (self.osrm_instance_region is None):
            return False

        return True


    def init_osrm_server(self):
        """Initialize a osrm server using the command osrm-routed. It will not start a new server if there is another one running.
        """
        command = ""
        command += self.osrm_routed_command_location + " "
        command += self.osrm_regions_map_files[self.osrm_instance_region] + " " 
        command += "--algorithm=MLD" + " "
        command += "--max-table-size=1000000" + " "
        command += "--ip=127.0.0.1" + " "
        command += "--port=6969" + " "
        command += "--mmap"

        if (self.running_osrm):
            # execution_log.info_log("Process not initiated. There is already a running osrm server.")
            return
        
        execution_log.info_log("Starting OSRM with command: \n    " + command)

        # The command below runs the server and shows output in the terminal
        # server_process = subprocess.Popen("exec " + command, shell=True)
        
        # The commands below runs the server and shows the output in a log file 
        self.log_file = open(self.log_file_path, "w")

        self.server_process = subprocess.Popen(
            "exec " + command, 
            shell=True, 
            stdout=self.log_file
        )

        self.running_osrm = True


    def finish_osrm_server(self):
        """Stop a osrm server if initialized
        """

        if (not self.running_osrm):
            return

        self.server_process.terminate()
        
        self.server_process = None
        self.running_osrm = False
        self.log_file.close()


    def send_request(self, url):
        total_time = 0
        has_response = False
        while (not has_response and total_time < 60):
            if (total_time > 0):
                execution_log.info_log(
                    "Communication with OSRM Failed. Retrying."
                )
            try:
                response = requests.get(url)
                has_response = True
            except Exception:
                time.sleep(1)
                total_time += 1
        
        return response


    def request_dist_and_time_remote(self, x, y):
        """Make a /route request to OSRM demo server and return distance and time between two points
        """
        # Avoids being blocked for sending too many requests to OSRM demo server
        time.sleep(random.randint(0,10))
        
        url = ""
        url += "http://router.project-osrm.org/route/v1/driving/"
        url += str(x[1]) + "," + str(x[0]) + ";" + str(y[1]) + "," + str(y[0])
        
        response = self.send_request(url)

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

    def request_dist_and_time_local(self, x, y):
        """Make a /route request to OSRM local server and return distance and time between two points
        """
        time.sleep((random.randint(0,10)/1000.0))
        url = ""
        url += "http://127.0.0.1:6969/route/v1/driving/"
        url += str(x[1]) + "," + str(x[0]) + ";" + str(y[1]) + "," + str(y[0])

        response = self.send_request(url)

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


    def request_dist_and_time(self, x, y):
        """Make a /route request to OSRM server and return distance and time between two points. The request will be remote if --run-distances-remote parameter is set, and locally otherwise.
        """
        calcuate_distance_local = self.distances_locally

        if (calcuate_distance_local):
            return self.request_dist_and_time_local(x, y)
        
        return self.request_dist_and_time_remote(x, y)


    def request_dist_and_time_from_source_local(self, source_position, points):
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
        
        response = self.send_request(url)

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

    def request_dist_and_time_from_source_remote(self, source_position, points):
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
        
        response = self.send_request(url)

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

    def calculate_dist_and_time_from_source(self, source_position, points):
        """Make a /table request to OSRM server and return distance and time between from a source to a list of points. The request will be remote if --run-distances-remote parameter is set, and locally otherwise.
        """
        calcuate_distance_local = self.distances_locally

        if (calcuate_distance_local):
            return self.request_dist_and_time_from_source_local(
                source_position, 
                points
            )

        return self.request_dist_and_time_from_source_remote(
            source_position, 
            points
        )

