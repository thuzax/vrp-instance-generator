import copy
import os
import random
import subprocess
import src.problems

from src.subproblems import SubProblem
from src.problems import *
from src import execution_log

class CVRPFilo(SubProblem):
    filo_command_location = None

    # from problem class
    points = None

    # generatad
    capacity = None
    demands = None

    # parameter
    cvrp_input_path = None
    cvrp_input_name = None
    cvrp_input_file = None

    def __init__(self):
        super().__init__("CVRP solved by FILO")


    def make_cvrp_file_text(self):
        """Make a string in CVRPLIB instances format
        """

        text = ""
        text += "NAME\t:\t" + self.cvrp_input_name
        text += "\n"
        text += "COMMENT\t:\t" + "\"\""
        text += "\n"
        text += "TYPE\t:\t" + "CVRP"
        text += "\n"
        text += "DIMENSION\t:\t" + str(len(self.points)+1)
        text += "\n"
        text += "EDGE_WEIGHT_TYPE\t:\t" + "EUC_2D"
        text += "\n"
        text += "CAPACITY\t:\t" + str(self.capacity)
        text += "\n"
        text += "NODE_COORD_SECTION"
        text += "\n"

        random_lat = random.randint(0, len(self.points)-1)
        random_lon = random.randint(0, len(self.points)-1)
        fake_depot = (self.points[random_lat][0], self.points[random_lon][1])

        text += str(1) + "\t" + str(fake_depot[0]) + "\t" + str(fake_depot[1])
        text += "\n"

        for i in range(len(self.points)):
            text += str(i+2) + "\t" + str(self.points[i][0]) 
            text += "\t" + str(self.points[i][1])
            text += "\n"
            
        text += "DEMAND_SECTION"
        text += "\n"

        text += str(1) + "\t" + str(0) + "\n"

        for i in range(len(self.points)):
            text += str(i+2) + "\t" + str(self.demands[i])
            text += "\n"

        text += "DEPOT_SECTION"
        text += "\n"
        text += str(1)
        text += "\n"
        text += str(-1)
        text += "\n"
        text += "EOF"
        text += "\n"

        return text

    def write_cvrp_file(self):
        """Write the file as a CVRP instances according to CVRPLIB instances
        """

        output_text = self.make_cvrp_file_text()

        with open(self.cvrp_input_file, "w") as output_file:
            output_file.write(output_text)


    def make_instance_file_name(self):

        if (self.cvrp_input_path[-1] != "/"):
            self.cvrp_input_path = self.cvrp_input_path + "/"

        
        self.cvrp_input_file = self.cvrp_input_path + "cvrp_" 
        self.cvrp_input_file += self.cvrp_input_name + ".vrp"


    def get_subproblem_instance(self):

        self.capacity = 1000000

        probabilities = [1, 0, 0, 0]
        self.demands = []
        for i in range(len(self.points)):
            self.demands.append(0)
            for probability in probabilities:
                p = random.randint(0,1000)/1000.0
                if (p <= probability):
                    self.demands[i] += 1

        self.make_instance_file_name()
        self.write_cvrp_file()

        
    
    def solve_instance(self):
        """Run the filo algorithm. It uses the variable filo_path, provided by the paths file.
        """

        instance = os.path.abspath(self.cvrp_input_file)
        output_path = os.path.abspath(self.cvrp_input_path) + "/"
        
        filo_path = self.filo_command_location

        command = ""
        command += filo_path + " "
        command += instance + " "
        command += "--parser X" + " "
        command += "--outpath " + output_path + " "

        # print()
        execution_log.info_log(
            "Starting filo with command: \n    " + command
        )


        # The command below runs the server and shows output in the terminal
        # filo_process = subprocess.Popen("exec " + command, shell=True)
        
        # The commands below runs the server and shows the output in a log file 
        # callend #osrm-server-log-file.txt
        log_name = output_path + "#filo_log_file_" 
        log_name += self.cvrp_input_name + ".log"
        filo_log = open(log_name, "w")
        filo_process = subprocess.Popen(
            "exec " + command, 
            shell=True, 
            stdout=filo_log
        )

        filo_process.wait()
    
    
    def get_subproblem_result(self):
        solution_file_name = self.cvrp_input_file + "_seed-0.vrp.sol"

        with open(solution_file_name, "r") as solution_file:
            routes_str = solution_file.read().split("\n")[:-1]
        
            routes = []

            for route_str in routes_str:
                nodes = route_str.split(":")[1].strip().split(" ")
                nodes = [int(node)-1 for node in nodes]

                nodes = set(nodes)

                routes.append(nodes)

            self.cvrp_routes = routes
        

    def get_dynamic_setting_elements(self):
        cvrp_elements_to_problem_elements = {
            "points" : "points",
            "cvrp_input_path" : "output_path",
            "cvrp_input_name" : "output_name"
        }

        return cvrp_elements_to_problem_elements

