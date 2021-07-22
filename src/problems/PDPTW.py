import copy
import json
from os import write

from src.problems.ProblemClass import ProblemClass

class PDPTW(ProblemClass):

    # Non-obrigatory Items
    cvrp_routes = None
    capacity = None
    pickups_and_deliveries = None
    demands = None

    services_times = None
    time_windows_pd = None
    planning_horizon = None
    time_windows_size = None


    def __init__(self):
        super().__init__(
            "Pickup and Delivery Problem" +
            "with Time Windows"
        )


    def get_constraints_generation_order(self):
        return [
            "HomogeneousCapacity",
            "PickupAndDelivery", 
            "ServiceTime",
            "TimeWindowsPD"
        ]


    def get_dynamic_setting_dict(self, constraint_class):

        dynamic_setting_dict = {}
        
        if (constraint_class == "PickupAndDelivery"):
            dynamic_setting_dict["points"] = (
                copy.deepcopy(self.points)
            )
            dynamic_setting_dict["cvrp_routes"] = (
                copy.deepcopy(self.cvrp_routes)
            )
            dynamic_setting_dict["distance_matrix"] = (
                copy.deepcopy(self.distance_matrix)
            )
        
        if (constraint_class == "ServiceTime"):
            dynamic_setting_dict["number_of_points"] = (
                copy.deepcopy(self.number_of_points)
            )

        if (constraint_class == "TimeWindowsPD"):
            dynamic_setting_dict["pickups_and_deliveries"] = (
                copy.deepcopy(self.pickups_and_deliveries)
            )
            dynamic_setting_dict["services_times"] = (
                copy.deepcopy(self.services_times)
            )
            dynamic_setting_dict["time_matrix"] = (
                copy.deepcopy(self.time_matrix)
            )

        return dynamic_setting_dict


    def update_problem_class(self, constraint_dict):
        for attrbute, value in constraint_dict.items():
            super().set_attribute(attrbute, value)


    def make_matrix_edges(self, edge_title, matrix, points_mapping=None):
        text = ""
        text += edge_title + "\n"

        if (points_mapping is None):
            
            for line in matrix:
                for i in range(len(line)-1):
                    item = int(line[i])
                    text += str(item) + " "
                text += str(int(line[-1]))
                text += "\n"
            
        else:
            for i in range(1, len(points_mapping)+1):
                point_index = points_mapping[i]

                for j in range(1, len(points_mapping)):
                    other_point_index = points_mapping[j]

                    value = int(matrix[point_index][other_point_index])

                    text += str(value) + " "

                other_point_index = points_mapping[len(points_mapping)]

                value = int(matrix[point_index][other_point_index])
                text += str(value) + " "
                text += "\n"


        return text


    def write_generic_file(self, output_file_name):
        text = ""
        text += "NAME : " + str(self.name)
        text += "\n"
        text += "LOCATION : " + str("")
        text += "\n"
        text += "COMMENT : " + str("")
        text += "\n"
        text += "TYPE : " + str("PDPTW")
        text += "\n"
        text += "SIZE : " + str(self.number_of_points)
        text += "\n"
        text += "DISTRIBUTION : " + str("")
        text += "\n"
        text += "DEPOT : " + str("")
        text += "\n"
        text += "ROUTE-TIME : " + str(self.planning_horizon)
        text += "\n"
        text += "TIME-WINDOW : " + str(self.time_windows_size)
        text += "\n"
        text += "CAPACITY : " + str(self.capacity)
        text += "\n"
        text += "FLEET-SIZE : " + str("")

        text += "}"
        
        text += "\n"

        text += "NODES"
        text += "\n"

        text_pickups = ""
        text_deliveries = ""
        i = 1

        map_file_nodes_to_points = {}

        for pickup, delivery in self.pickups_and_deliveries:
            tw_pickup, tw_delivery = self.time_windows_pd[(pickup, delivery)]
            j = i + len(self.pickups_and_deliveries) # pair delivery id
            
            text_pickups += str(i) # id
            text_pickups += " "
            text_pickups += str(self.points[pickup][0])  # latitude
            text_pickups += " "
            text_pickups += str(self.points[pickup][1])  # longitude
            text_pickups += " "
            text_pickups += str(self.demands[pickup]) # demand
            text_pickups += " "
            text_pickups += str(tw_pickup[0]) # start of time window
            text_pickups += " "
            text_pickups += str(tw_pickup[1]) # end of time window
            text_pickups += " "
            text_pickups += str(self.services_times[pickup]) # service time
            text_pickups += " "
            text_pickups += str(0) # pick pair id (0 because the pair is deliv)
            text_pickups += " "
            
            text_pickups += str(j) # delivery pair id
            
            text_pickups += "\n"

            map_file_nodes_to_points[i] = pickup

            text_deliveries += str(j) # id
            text_deliveries += " "
            text_deliveries += str(self.points[delivery][0])  # latitude
            text_deliveries += " "
            text_deliveries += str(self.points[delivery][1])  # longitude
            text_deliveries += " "
            text_deliveries += str(self.demands[delivery]) # demand
            text_deliveries += " "
            text_deliveries += str(tw_delivery[0]) # start of time window
            text_deliveries += " "
            text_deliveries += str(tw_delivery[1]) # end of time window
            text_deliveries += " "
            text_deliveries += str(self.services_times[delivery]) # service time
            text_deliveries += " "
            text_deliveries += str(i) # pickup pair id
            text_deliveries += " "
            text_deliveries += str(0) # deliv pair id (0 because the pair is pick)

            text_deliveries += "\n"

            map_file_nodes_to_points[j] = delivery

            i += 1

        text += text_pickups + text_deliveries

        edges_distance = self.make_matrix_edges(
            "EDGES_DISTANCE", 
            self.distance_matrix, 
            map_file_nodes_to_points
        )

        edges_time = self.make_matrix_edges(
            "EDGES_TIME", 
            self.time_matrix, 
            map_file_nodes_to_points
        )

        text += edges_distance
        text += edges_time
        text += "EOF"

        if (self.output_path[-1] != "/"):
            self.output_path += "/"
        
        with open(output_file_name, "w") as output_file:
            output_file.write(text)


    def write_json_file(self,output_file_name):
        output_dict = {}

        output_dict["points"] = copy.deepcopy(self.points)

        output_dict["points"] = [[x,y] for x, y in output_dict["points"]]

        output_dict["number_of_points"] = self.number_of_points

        output_dict["distance_matrix"] = copy.deepcopy(self.distance_matrix)
        output_dict["distance_matrix"] = (
            self.distance_matrix.astype(int).tolist()
        )

        output_dict["time_matrix"] = copy.deepcopy(self.time_matrix)
        output_dict["time_matrix"] = self.time_matrix.astype(int).tolist()

        output_dict["capacity"] = self.capacity

        output_dict["pickups_and_deliveries"] = copy.deepcopy(
            self.pickups_and_deliveries
        )

        output_dict["pickups_and_deliveries"] = [
            [int(x), int(y)] for x, y in output_dict["pickups_and_deliveries"]
        ]
        
        output_dict["demands"] = {}
        for key, value in self.demands.items():
            output_dict["demands"][int(key)] = int(value)
            

        output_dict["services_times"] = copy.deepcopy(self.services_times)
        output_dict["services_times"] = self.services_times.tolist()

        time_windows_dict = {}
        for pair, tws in self.time_windows_pd.items():
            time_windows_dict[int(pair[0])] = [tws[0][0], tws[0][1]]
            time_windows_dict[int(pair[1])] = [tws[1][0], tws[1][1]]
        
        output_dict["time_windows_pd"] = time_windows_dict


        if (self.output_path[-1] != "/"):
            self.output_path += "/"

        with open(output_file_name, "w") as output_file:
            output_file.write(json.dumps(output_dict))



