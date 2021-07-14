import random
import numpy
import matrices_calculation

from src import global_parameters
from src import arguments_handler
from src import generation_manager
from src import vrp_files_manager
from src import osrm_manager
from src import filo_manager

from constraints import *

from problems import *
from points_generation_managers import *
from matrices_calculation import *


def generate_points():
    points_generator_manager = PointsGeneratorManager()
    problem_class = ProblemClass()
    
    points_generator_manager.read_file()
    
    points = points_generator_manager.select_points(
        problem_class.number_of_points
    )

    points_generator_manager.write_selected_items(
        problem_class.output_path, 
        problem_class.output_name
    )

    problem_class.set_attribute("points", points)
    problem_class.set_attribute("number_of_points", len(points))


def calculate_distances():
    matrices_calculator = DistancesAndTimesCalculator()

    problem_class = ProblemClass()

    matrices_calculator.set_attribute("points", problem_class.points)

    distance_matrix, time_matrix = (
        matrices_calculator.calculate_distances_and_times()
    )

    problem_class.set_attribute("distance_matrix", distance_matrix)
    problem_class.set_attribute("time_matrix", time_matrix)



def generate_constraints():
    problem_class = ProblemClass()
    
    constraints_objects = problem_class.constraints_objects
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
    global_parameters.init()
    arguments_handler.parse_command_line_arguments()
    arguments_handler.read_configuration_file()
    arguments_handler.read_paths_file()
    arguments_handler.read_configurations()


    random.seed(global_parameters.random_seed())
    numpy.random.seed(global_parameters.random_seed())

    exception = None

    try:
        generate_points()
        calculate_distances()
        problem_class = ProblemClass()

        cvrp_capacity = generation_manager.generate_cvrp_capacity()
        cvrp_demands = generation_manager.generate_cvrp_demands(
            problem_class.number_of_points
        )

        cvrp_file_name = problem_class.output_path + "/" + "cvrp_" 
        cvrp_file_name += problem_class.output_name + ".vrp"
        
        vrp_files_manager.write_cvrp_file(
                            cvrp_file_name,
                            problem_class.number_of_points, 
                            cvrp_capacity, 
                            problem_class.points, 
                            cvrp_demands
                        )

        filo_manager.run_filo(cvrp_file_name, problem_class.output_path)

        routes = vrp_files_manager.read_cvrp_solution_routes(cvrp_file_name)

        problem_class.set_attribute("cvrp_routes", routes)

        generate_constraints()

        problem_class.write_file()



    except Exception as e:
        exception = e
    finally:
        DistancesAndTimesCalculator().__del__()

        if (exception is not None):
            raise exception