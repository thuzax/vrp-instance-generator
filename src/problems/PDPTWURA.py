import copy
import json

from src.problems.ProblemClass import ProblemClass

class PDPTWURA(ProblemClass):

    # Non-obrigatory Items
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
    
    number_of_depots = None

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


    def update_problem_class(self, constraint_dict):
        for attrbute, value in constraint_dict.items():
            self.set_attribute(attrbute, value)


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
        
        with open(output_file_name, "w") as output_file:
            output_file.write(text)


    def write_json_file(self, output_file_name):
        output_dict = {}

        mapping = {}
        reverse_mapping = {}
        if (len(self.depots) == 0):
            position = 1
        else:
            position = self.points_indices[0]

        initial_value = 0 if (len(self.depots) > 0) else 1

        for i, j in self.pickups_and_deliveries:
            mapping[position] = i - len(self.depots)
            mapping[position + int(len(self.points)/2)] = j - len(self.depots)
            position += 1

        list_points = [
            [
                self.points[mapping[i+initial_value]][0], 
                self.points[mapping[i+initial_value]][1]
            ] 
            for i in self.points_indices
        ]

        output_dict["points"] = {}

        for i in range(len(self.depots)):
            output_dict["points"][i] = self.depots[i]

        for i in self.points_indices:
            output_dict["points"][i+initial_value] = (
                list_points[i-len(self.depots)]
            )

        output_dict["number_of_points"] = (
            len(self.points) + len(self.depots)
        )

        if (len(self.depots) == 1):
            output_dict["depot"] = 0
        elif (len(self.depots) > 1):
            output_dict["depots"] = [i for i in range(len(self.depots))]

        output_dict["distance_matrix"] = {}
        output_dict["time_matrix"] = {}

        for i in range(len(self.depots)):
            output_dict["distance_matrix"][i] = {}
            output_dict["time_matrix"][i] = {}
            
            for j in range(len(self.depots)):
                dist_value = self.distance_matrix[i][j]
                dist_value = int(dist_value)
                output_dict["distance_matrix"][i][j] = dist_value

                time_value = self.time_matrix[i][j]
                time_value = int(time_value)
                output_dict["time_matrix"][i][j] = time_value

            for j in self.points_indices:
                pos_j = j + initial_value
                index_j = mapping[pos_j] + len(self.depots)
                
                dist_value = self.distance_matrix[i][index_j]
                dist_value = int(dist_value)
                output_dict["distance_matrix"][i][pos_j] = dist_value

                time_value = self.time_matrix[i][index_j]
                time_value = int(time_value)
                output_dict["time_matrix"][i][pos_j] = time_value

        for i in self.points_indices:
            pos_i = i + initial_value
            index_i = mapping[pos_i] + len(self.depots)
            output_dict["distance_matrix"][pos_i] = {}
            output_dict["time_matrix"][pos_i] = {}

            for j in range(len(self.depots)):
                dist_value = self.distance_matrix[index_i][j]
                dist_value = int(dist_value)
                output_dict["distance_matrix"][pos_i][j] = dist_value

                time_value = self.time_matrix[index_i][j]
                time_value = int(time_value)
                output_dict["time_matrix"][pos_i][j] = time_value

            for j in self.points_indices:
                pos_j = j + initial_value
                
                index_j = mapping[pos_j] + len(self.depots)
                
                dist_value = self.distance_matrix[index_i][index_j]
                dist_value = int(dist_value)
                output_dict["distance_matrix"][pos_i][pos_j] = dist_value

                time_value = self.time_matrix[index_i][index_j]
                time_value = int(time_value)
                output_dict["time_matrix"][pos_i][pos_j] = time_value

        output_dict["capacity"] = self.capacity

        output_dict["pickups_and_deliveries"] = []

        for i in range(len(self.pickups_and_deliveries)):
            pickup = i + len(self.depots) + initial_value
            delivery = pickup + len(self.pickups_and_deliveries)
            output_dict["pickups_and_deliveries"].append([pickup, delivery])

        output_dict["pickups_and_deliveries"] = [
            [int(x), int(y)] for x, y in output_dict["pickups_and_deliveries"]
        ]

        output_dict["demands"] = {}
        for i in self.points_indices:
            output_dict["demands"][i+initial_value] = (
                self.demands[i]
            )

        output_dict["services_times"] = {}
        for i in self.points_indices:
            output_dict["services_times"][i+initial_value] = (
                self.services_times[i]
            )

        time_windows_dict = {}

        for i in range(len(self.pickups_and_deliveries)):
            pick_pos = i + len(self.depots) + initial_value
            pick = self.pickups_and_deliveries[i][0]
            deli_pos = pick_pos + len(self.pickups_and_deliveries)
            deli = self.pickups_and_deliveries[i][1]
            
            tws = self.time_windows_pd[(pick, deli)]

            time_windows_dict[pick_pos] = [tws[0][0], tws[0][1]]
            time_windows_dict[deli_pos] = [tws[1][0], tws[1][1]]
        
        output_dict["time_windows_pd"] = time_windows_dict

        output_dict["planning_horizon"] = int(self.planning_horizon)
        output_dict["time_windows_size"] = int(self.time_windows_size)
        
        list_urb_rur = [
            0 
            if (
                self.urban_rural_aptitude[
                    mapping[self.points_indices[i]+initial_value]
                ] 
                == "u"
            )
            else 
            1 
            for i in range(len(self.urban_rural_aptitude))
        ]


        print(mapping)
        print(self.urban_rural_aptitude)
        output_dict["urban_rural_aptitude"] = {}
        for i in self.points_indices:
            output_dict["urban_rural_aptitude"][i+initial_value] = (
                list_urb_rur[i-len(self.depots)]
            )

        output_dict["fleets_size"] = copy.deepcopy(self.fleets_sizes)

        if (self.output_path[-1] != "/"):
            self.output_path += "/"

        with open(output_file_name, "w") as output_file:
            output_file.write(json.dumps(output_dict))
            
