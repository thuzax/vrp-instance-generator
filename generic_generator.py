import random
import numpy
import pprint
import copy

from src import global_parameters
from src import arguments_handler
from src import status_variables
from src import csv_manager
from src import filter_csv
from src import generation_manager
from src import vrp_files_manager
from src import osrm_manager
from src import filo_manager
from problems import ProblemInstance

from constraints import *


def generate_constraints(constraints_objects):
    problem_class = ProblemInstance.Instance()
    generation_order = problem_class.get_constraints_generation_order()

    for constraint_class in generation_order:
        dict_to_set_dynamic = problem_class.get_dynamic_setting_dict(
            constraint_class
        )

        constraint_object = constraints_objects[constraint_class]

        for attribute, value in dict_to_set_dynamic.items():
            constraint_object.set_attribute(
                attribute,
                value
            )
        
        constraint_dict = constraint_object.get_constraint()
        problem_class.update_problem_class(constraint_dict)


if __name__ == "__main__":
    problem_class = ProblemInstance.Instance()
    global_parameters.init()
    arguments_handler.parse_command_line_arguments()
    arguments_handler.read_configuration_file()
    arguments_handler.read_paths_file()
    arguments_handler.read_constraints_config_file()

    random.seed(global_parameters.random_seed())
    numpy.random.seed(global_parameters.random_seed())

    exception = None

    try:
        status_variables.init()

        osrm_manager.init_osrm_server()
        

        # read input
        data = csv_manager.read_input_file()
        
        # filter data
        data = filter_csv.filter_data(data)

        # # choose the random address/points
        data = generation_manager.draw_instance_elements(data)

        points = csv_manager.get_points_coordinates(data)
        
        problem_class.set_attribute("points", points)
        problem_class.set_attribute("number_of_points", len(points))

        output_path = global_parameters.output_path()
        output_name = global_parameters.output_name()
        output_size = global_parameters.output_size()

        # write data in csv file
        csv_manager.write_output_file(data, output_path + "/" + output_name)

        distance_matrix, time_matrix = generation_manager.calculate_matrices(
                                                            points
                                                        )
        problem_class.set_attribute("distance_matrix", distance_matrix)
        problem_class.set_attribute("time_matrix", time_matrix)

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

        problem_class.set_attribute("cvrp_routes", routes)

        constraints_objects = global_parameters.constraints_objects()

        generate_constraints(constraints_objects)

        problem_class.write_text_file(output_path, "teste")

        # pprint.pprint(problem_class.__dict__, indent=2)


    except Exception as e:
        exception = e
    finally:
        osrm_manager.finish_osrm_server()

        if (exception is not None):
            raise exception