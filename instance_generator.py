import random
import numpy

from src import global_parameters
from src import arguments_handler
from src import status_variables
from src import csv_manager
from src import filter_csv
from src import generation_manager
from src import vrp_files_manager
from src import osrm_manager
from src import filo_manager


if __name__=="__main__":
    global_parameters.init()
    arguments_handler.parse_command_line_arguments()
    arguments_handler.read_configuration_file()
    arguments_handler.read_paths_file()

    random.seed(global_parameters.random_seed())
    numpy.random.seed(global_parameters.random_seed())

    exception = None

    status_variables.init()
    

    try:
        osrm_manager.init_osrm_server()
        

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

        distance_matrix, time_matrix = generation_manager.calculate_matrices(
                                                            points
                                                        )
        # print(distance_matrix)
        # print(time_matrix)

        cvrp_capacity = generation_manager.generate_cvrp_capacity()
        cvrp_demands = generation_manager.generate_cvrp_demands(output_size)

        cvrp_file_name = output_path + "/" + "cvrp_" + output_name + ".vrp"
        
        vrp_files_manager.write_cvrp_file(
                            cvrp_file_name,
                            output_size, 
                            cvrp_capacity, 
                            points, 
                            cvrp_demands
                        )

        filo_manager.run_filo(cvrp_file_name, output_path)

        routes = vrp_files_manager.read_cvrp_solution_routes(cvrp_file_name)
        
        route_pd = generation_manager.generate_pickups_and_deliveries_by_routes(
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

        pickups_and_deliveries = route_pd + dist_pds + rand_pds

        services_times = generation_manager.generate_services_times(
                                                points
                                            )

        time_windows = generation_manager.generate_time_windows(
                                            pickups_and_deliveries,
                                            points,
                                            services_times,
                                            time_matrix
                                        )

        clients_classif = generation_manager.generate_urb_rur_aptitude(
                                                    points
                                                )

        fleet_size = (
                    generation_manager.generate_fleets_sizes(
                        pickups_and_deliveries
                    )
        )

        urban_fleet_size, rural_fleet_size = generation_manager.divide_fleet(
                                                fleet_size, 
                                                clients_classif,
                                            )



        pdtwlhf_file_name = output_path + "/" + "pdtwhf_" + output_name + ".vrp"
        instance_name = output_name
        vrp_files_manager.write_pd_tw_lhf(
                            points=points,
                            pickups_and_deliveries=pickups_and_deliveries,
                            service_times=services_times,
                            time_windows=time_windows,
                            clients_classif=clients_classif,
                            fleets_sizes=[urban_fleet_size, rural_fleet_size],
                            distance_matrix=distance_matrix,
                            time_matrix=time_matrix,
                            output_name=pdtwlhf_file_name,
                            instance_name=instance_name
                        )

        print(points)
        print(pickups_and_deliveries)
        print(services_times)
        print(time_windows)
        print(clients_classif)
        print(urban_fleet_size, rural_fleet_size)

    except Exception as e:
        exception = e
    finally:
        osrm_manager.finish_osrm_server()

        if (exception is not None):
            raise exception

