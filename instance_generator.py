import random

from src import global_parameters
from src import arguments_handler
from src import status_variables
from src import csv_manager
from src import filter_csv
from src import generation_manager
from src import cvrp_file_manager
from src import osrm_manager
from src import filo_manager



if __name__=="__main__":
    global_parameters.init()
    arguments_handler.parse_command_line_arguments()
    arguments_handler.read_configuration_file()
    arguments_handler.read_paths_file()

    status_variables.init()

    osrm_manager.init_osrm_server()
    


    random.seed(0)

    # read input
    data = csv_manager.read_input_file()
    
    # filter data
    data = filter_csv.filter_data(data)


    # # choose the random address/points
    data = generation_manager.draw_instance_elements(data)

    points = csv_manager.get_points_coordinates(data)
    
    output_path = global_parameters.output_path()
    output_name = global_parameters.output_name()
    output_size = global_parameters.output_size()

    # write data in csv file
    csv_manager.write_output_file(data, output_path + "/" + output_name)

    distance_matrix, time_matrix = generation_manager.calculate_matrices(points)
    # print(distance_matrix)
    # print(time_matrix)



    cvrp_capacity = generation_manager.generate_cvrp_capacity()
    cvrp_demands = generation_manager.generate_cvrp_demands(output_size)


    cvrp_file_name = output_path + "/" + "cvrp_" + output_name + ".vrp"
    
    print(cvrp_file_name)

    cvrp_file_manager.write_file(
                        cvrp_file_name,
                        output_size, 
                        cvrp_capacity, 
                        points, 
                        cvrp_demands
                    )

    filo_manager.run_filo(cvrp_file_name, output_path)

    routes = cvrp_file_manager.read_solution_routes(cvrp_file_name)
    
    route_pds = generation_manager.generate_pickups_and_deliveries_by_routes(
                                    routes
                                )
    
    distance_pd = global_parameters.max_distance_pd()
    dist_pds = generation_manager.generate_pickups_and_deliveries_by_distance(
                                    distance_pd,
                                    distance_matrix
                                )

    rand_pds = generation_manager.generate_pickups_and_deliveries_randomly(
                                    output_size
                                )

    pickups_and_deliveries = route_pds + dist_pds + rand_pds

    print(pickups_and_deliveries)

    osrm_manager.finish_osrm_server()

