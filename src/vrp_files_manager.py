import random
import numpy
from numpy.lib.polynomial import polymul

from progress.bar import Bar

from src import global_parameters
from src import execution_log



def make_header(
    instance_name, 
    comment, 
    instance_type, 
    number_of_points, 
    distribution,
    depot,
    time_horizon,
    time_window_size,
    capacity,
    fleets_sizes
):
    text = ""
    text += "NAME : " + str(instance_name)
    text += "\n"
    text += "LOCATION : " + str("")
    text += "\n"
    text += "COMMENT : " + str(comment)
    text += "\n"
    text += "TYPE : " + str(instance_type)
    text += "\n"
    text += "SIZE : " + str(number_of_points)
    text += "\n"
    text += "DISTRIBUTION : " + str(distribution)
    text += "\n"
    text += "DEPOT : " + str(depot)
    text += "\n"
    text += "ROUTE-TIME : " + str(time_horizon)
    text += "\n"
    text += "TIME-WINDOW : " + str(time_window_size)
    text += "\n"
    text += "CAPACITY : " + str(capacity)
    text += "\n"
    text += "FLEET-SIZE : " + " ".join(
                                        [str(fleet_size) 
                                        for fleet_size in fleets_sizes]
                                    )
    text += "\n"
    
    return text


def make_cvrp_file_text(name,size, capacity, points, demands):
    """Make a string in CVRPLIB instances format
    """

    text = ""
    text += "NAME\t:\t" + name
    text += "\n"
    text += "COMMENT\t:\t" + "\"\""
    text += "\n"
    text += "TYPE\t:\t" + "CVRP"
    text += "\n"
    text += "DIMENSION\t:\t" + str(size+1)
    text += "\n"
    text += "EDGE_WEIGHT_TYPE\t:\t" + "EUC_2D"
    text += "\n"
    text += "CAPACITY\t:\t" + str(capacity)
    text += "\n"
    text += "NODE_COORD_SECTION"
    text += "\n"

    random_lat = random.randint(0, len(points)-1)
    random_lon = random.randint(0, len(points)-1)
    fake_depot = (points[random_lat][0], points[random_lon][1])

    text += str(1) + "\t" + str(fake_depot[0]) + "\t" + str(fake_depot[1])
    text += "\n"

    for i in range(size):
        text += str(i+2) + "\t" + str(points[i][0]) + "\t" + str(points[i][1])
        text += "\n"
        
    text += "DEMAND_SECTION"
    text += "\n"

    text += str(1) + "\t" + str(0) + "\n"

    for i in range(size):
        text += str(i+2) + "\t" + str(demands[i])
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

def write_cvrp_file(output_file_name, size, capacity, points, demands):
    """Write the file as a CVRP instances according to CVRPLIB instances
    """

    execution_log.info_log("Writing CVRP file...")

    output_text = make_cvrp_file_text(
                    output_file_name.split("/")[-1].split(".")[0], 
                    size, 
                    capacity, 
                    points, 
                    demands
                )

    with open(output_file_name, "w") as output_file:
        output_file.write(output_text)
    
    execution_log.info_log("Done.")


def read_cvrp_solution_routes(origin_file_name):
    solution_file_name = origin_file_name + "_seed-0.vrp.sol"

    with open(solution_file_name, "r") as solution_file:
        routes_str = solution_file.read().split("\n")[:-1]
    
    routes = []

    for route_str in routes_str:
        nodes = route_str.split(":")[1].strip().split(" ")
        nodes = [int(node)-1 for node in nodes]

        nodes = set(nodes)

        routes.append(nodes)

    return routes


def transform_client_classif_in_ids(client_classif):
    if (client_classif == "u"):
        return 0
    if (client_classif == "r"):
        return 1
    return -1

def make_pickups_and_deliveries_nodes(
    points,
    pickup_and_deliveries,
    service_times,
    time_windows,
    clients_classif
):
    text = ""
    text += "NODES"
    text += "\n"

    text_pickups = ""
    text_deliveries = ""
    i = 1

    map_file_nodes_to_points = {}

    for pickup, delivery in pickup_and_deliveries:
        tw_pickup, tw_delivery = time_windows[(pickup, delivery)]
        
        text_pickups += str(i) # id
        text_pickups += " "
        text_pickups += str(points[pickup][0])  # latitude
        text_pickups += " "
        text_pickups += str(points[pickup][1])  # longitude
        text_pickups += " "
        text_pickups += str(0) # demand
        text_pickups += " "
        text_pickups += str(tw_pickup[0]) # start of time window
        text_pickups += " "
        text_pickups += str(tw_pickup[1]) # end of time window
        text_pickups += " "
        text_pickups += str(service_times[pickup]) # service time
        text_pickups += " "
        text_pickups += str(0) # pick pair id (0 because the pair is deliv)
        text_pickups += " "
        text_pickups += str(i + len(pickup_and_deliveries)) # delivery pair id
        text_pickups += " "
        text_pickups += str(transform_client_classif_in_ids(
                                clients_classif[pickup]
                        )) # 0 if urban, 1 if rural
        text_pickups += "\n"

        map_file_nodes_to_points[i] = pickup
        
        j = i + len(pickup_and_deliveries)

        text_deliveries += str(j) # id
        text_deliveries += " "
        text_deliveries += str(points[delivery][0])  # latitude
        text_deliveries += " "
        text_deliveries += str(points[delivery][1])  # longitude
        text_deliveries += " "
        text_deliveries += str(0) # demand
        text_deliveries += " "
        text_deliveries += str(tw_delivery[0]) # start of time window
        text_deliveries += " "
        text_deliveries += str(tw_delivery[1]) # end of time window
        text_deliveries += " "
        text_deliveries += str(service_times[delivery]) # service time
        text_deliveries += " "
        text_deliveries += str(i) # pickup pair id
        text_deliveries += " "
        text_deliveries += str(0) # deliv pair id (0 because the pair is pick)
        text_deliveries += " "
        text_deliveries += str(transform_client_classif_in_ids(
                            clients_classif[delivery]
                        )) # 0 if urban, 1 if rural
        text_deliveries += "\n"

        map_file_nodes_to_points[j] = delivery

        i += 1

    text += text_pickups + text_deliveries

    return (text, map_file_nodes_to_points)


def make_edges(edge_title, matrix, points_mapping=None):
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
    


# Write a file on the format of a uncapactitaded pickup and delivery with time 
# windows (including service times) and limited hybrid fleet
def write_pd_tw_lhf(
    points,
    pickups_and_deliveries,
    service_times,
    time_windows,
    clients_classif,
    fleets_sizes,
    distance_matrix,
    time_matrix,
    output_name,
    instance_name
):
    execution_log.info_log("Writing PDPTWLHF file...")
    bar = Bar("Processing:", max=4,suffix='%(percent)d%%')
    
    header = make_header(
            instance_name=instance_name,
            comment="",
            instance_type="PDPTWLHF",
            number_of_points=(len(pickups_and_deliveries)*2),
            distribution="",
            depot="",
            time_horizon=global_parameters.time_windows_horizon(),
            time_window_size=global_parameters.time_windows_size(),
            capacity="",
            fleets_sizes=fleets_sizes
        )

    bar.next()


    nodes, nodes_to_points_mapping = make_pickups_and_deliveries_nodes(
                points=points,
                pickup_and_deliveries=pickups_and_deliveries,
                service_times=service_times,
                time_windows=time_windows,
                clients_classif=clients_classif
            )

    bar.next()

    edges_distance = make_edges(
                        "EDGES_DISTANCE", 
                        distance_matrix, 
                        nodes_to_points_mapping
                    )

    bar.next()

    edges_time = make_edges(
                    "EDGES_TIME", 
                    time_matrix, 
                    nodes_to_points_mapping
                )

    bar.next()


    text = ""
    text += header
    text += nodes
    text += edges_distance
    text += edges_time
    text += "EOF"

    with open(output_name, "w") as output_file:
        output_file.write(text)

    bar.finish()
    execution_log.info_log("Done.")
