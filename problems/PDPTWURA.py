import copy
import json

from problems.ProblemClass import ProblemClass

class PDPTWURA(ProblemClass):

    # Non-obrigatory Items
    time_matrix = None

    cvrp_routes = None
    capacity = None
    pickups_and_deliveries = None
    demands = None

    services_times = None
    time_windows_pd = None
    planning_horizon = None
    time_windows_size = None

    urban_rural_aptitude = None
    fleets_sizes = None
    
    def __init__(self):
        super().__init__(
            "Pickup and Delivery Problem" +
            "with Time Windows" +
            "and Urban/Rural Aptitude"
        )


    def get_constraints_generation_order(self):
        return [
            "HomogeneousCapacity",
            "PickupAndDelivery", 
            "ServiceTime",
            "TimeWindowsPD",
            "UrbanRuralAptitude",
            "LimitedFleetUrbanRural"
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

        if (constraint_class == "UrbanRuralAptitude"):
            dynamic_setting_dict["points"] = (
                copy.deepcopy(self.points)
            )

        if (constraint_class == "LimitedFleetUrbanRural"):
            dynamic_setting_dict["urban_rural_aptitude"] = (
                copy.deepcopy(self.urban_rural_aptitude)
            )
            dynamic_setting_dict["cvrp_routes"] = (
                copy.deepcopy(self.cvrp_routes)
            )

        return dynamic_setting_dict


    def update_problem_class(self, constraint_dict):
        for attrbute, value in constraint_dict.items():
            self.set_attribute(attrbute, value)


    def write_text_file(self):
        text = ""
        text += "NAME : " + str(self.name)
        text += "\n"
        text += "LOCATION : " + str("")
        text += "\n"
        text += "COMMENT : " + str("")
        text += "\n"
        text += "TYPE : " + str("PDPTWURA")
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
        text += "FLEET-SIZE : {" 
        text += ",".join([
                str(fleet_size) 
                for fleet_size in self.fleets_sizes.values()
        ])

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

            text_pickups += " "
            
            text_pickups += str(
                0 if self.urban_rural_aptitude[pickup] == "u" else 1
            ) # 0 if urban, 1 if rural
            
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
            text_deliveries += " "
            text_deliveries += str(
                0 if self.urban_rural_aptitude[delivery] == "u" else 1
            ) # 0 if urban, 1 if rural
            
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
        
        with open(self.output_path + self.output_name + ".pdptwura", "w") as output_file:
            output_file.write(text)


    def write_json_file(self):
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
            [x,y] for x, y in output_dict["pickups_and_deliveries"]
        ]
        
        output_dict["demands"] = copy.deepcopy(
            self.demands
        )

        output_dict["demands"] = self.demands

        output_dict["services_times"] = copy.deepcopy(self.services_times)
        
        output_dict["services_times"] = self.services_times.tolist()

        time_windows_dict = {}
        for pair, tws in self.time_windows_pd.items():
            time_windows_dict[pair[0]] = [tws[0][0], tws[0][1]]
            time_windows_dict[pair[1]] = [tws[1][0], tws[1][1]]
        
        output_dict["time_windows_pd"] = time_windows_dict

        output_dict["urban_rural_aptitude"] = [
            0 if aptitude == "u" else 1
            for aptitude in self.urban_rural_aptitude
        ]

        output_dict["fleets_size"] = copy.deepcopy(self.fleets_sizes)

        if (self.output_path[-1] != "/"):
            self.output_path += "/"

        with open(self.output_path + self.output_name + ".json", "w") as output_file:
            output_file.write(json.dumps(output_dict))
