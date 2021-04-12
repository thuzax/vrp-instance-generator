import random
import copy

from src import execution_log

def make_file_text(name,size, capacity, points, demands):
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
        text += str(i+1) + "\t" + str(points[i][0]) + "\t" + str(points[i][1])
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

def write_file(output_file_name, size, capacity, points, demands):
    """Write the file as a CVRP instances according to CVRPLIB instances
    """

    execution_log.info_log("Writing CVRP file...")

    output_text = make_file_text(
                    output_file_name.split("/")[-1].split(".")[0], 
                    size, 
                    capacity, 
                    points, 
                    demands
                )

    with open(output_file_name, "w") as output_file:
        output_file.write(output_text)
    
    execution_log.info_log("Done.")


def read_solution_routes(origin_file_name):
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

    