import random
import numpy
import time

from src import arguments_handler
from src import execution_log

from src.constraints import *
from src.problems import *
from src.points_generation_managers import *
from src.matrices_calculation import *


def generate_points():
    execution_log.info_log("Starting Points Extraction...")
    points_generator_manager = PointsGeneratorManager()
    problem_class = ProblemClass()
    
    execution_log.info_log("Reading and Filtering Input File...")
    points_generator_manager.read_file()
    
    execution_log.info_log("Selecting Points...")
    points = points_generator_manager.select_points(
        problem_class.number_of_points
    )

    execution_log.info_log("Writing Selected Points...")
    points_generator_manager.write_selected_items(
        problem_class.output_path, 
        problem_class.output_name
    )

    execution_log.info_log("Saving Values...")
    problem_class.set_attribute("points", points)
    problem_class.set_attribute("number_of_points", len(points))

    execution_log.info_log("*Points Extraction Finished.*")


def calculate_distances():
    execution_log.info_log("Starting Distances Calculation...")
    matrices_calculator = DistancesAndTimesCalculator()
    problem_class = ProblemClass()

    execution_log.info_log("Updating Dynamic Values...")
    matrices_calculator.set_attribute("points", problem_class.points)

    execution_log.info_log("Calculating Distances...")
    distance_matrix, time_matrix = (
        matrices_calculator.calculate_distances_and_times()
    )

    execution_log.info_log("Saving Distance and Time Matrices...")
    problem_class.set_attribute("distance_matrix", distance_matrix)
    problem_class.set_attribute("time_matrix", time_matrix)

    execution_log.info_log("*Distances Calculation Finished.*")


def solve_constraints_subproblems():
    execution_log.info_log("Starting Subproblems Resolution...")
    problem_class = ProblemClass()
    subproblems = problem_class.subproblems

    execution_log.info_log("Solving Subproblems:")
    for subproblem in subproblems:
        execution_log.info_log(
            "Solving: " 
            + subproblem.__class__.__name__ 
            + "..."
        )
        
        execution_log.info_log("Saving Subproblem Output...")

        dynamic_attributes = subproblem.get_dynamic_setting_elements()
        for subprob_attribute, prob_attribute in dynamic_attributes.items():
            subproblem.set_attribute(
                subprob_attribute, 
                getattr(problem_class, prob_attribute)
            )

        
        dict_solution = subproblem.solve_subproblem()
        for attribute, value in dict_solution.items():
            problem_class.set_attribute(attribute, value)
        
        execution_log.info_log("Subproblem Solved.")
    
    execution_log.info_log("*Subproblems Resolution Finished.*")


def generate_constraints():
    execution_log.info_log("Generating Constraints...")
    problem_class = ProblemClass()
    
    constraints_objects = problem_class.constraints_objects
    generation_order = problem_class.get_constraints_generation_order()

    for constraint_class in generation_order:
        execution_log.info_log("Updating Dynamic Values...")
        dict_to_set_dynamic = problem_class.get_dynamic_setting_dict(
            constraint_class
        )

        constraint_object = constraints_objects[constraint_class]


        for attribute, value in dict_to_set_dynamic.items():
            constraint_object.set_attribute(
                attribute,
                value
            )

        execution_log.info_log("Generating " + constraint_class + "...")
        constraint_dict = constraint_object.get_constraint()
        execution_log.info_log("Saving Constraint Attributes...")
        problem_class.update_problem_class(constraint_dict)
        execution_log.info_log("Constraint Generated.")

    execution_log.info_log("*Constraints Generation Finished.*")


def write_file():
    execution_log.info_log("Writing Output File...")
    problem_class = ProblemClass()
    problem_class.write_file()
    execution_log.info_log("*Output File Written*")


if __name__ == "__main__":
    execution_log.info_log("Starting Program")
    start_time = time.time()

    execution_log.info_log("Reading Input Parameters...")
    arguments = arguments_handler.parse_command_line_arguments()
    arguments_handler.read_configurations(arguments)

    execution_log.info_log("Setting Random Seed")
    random.seed(arguments["seed"])
    numpy.random.seed(arguments["seed"])

    exception = None

    try:
        execution_log.info_log("Starting Generation...")
        generate_points()
        calculate_distances()
        solve_constraints_subproblems()
        generate_constraints()
        write_file()
        execution_log.info_log("*Generation Finished.*")

    except Exception as e:
        exception = e
    
    finally:
        if (exception is None):
            execution_log.info_log("Writting Running Data...")
            end_time = time.time()
            total_time = end_time - start_time
            running_data = {
                "seed" : arguments["seed"],
                "time" : total_time
            }
            problem_class = ProblemClass()
            problem_class.write_final_data(running_data)
            execution_log.info_log("*Running Data Written.*")
        
        DistancesAndTimesCalculator().__del__()
        execution_log.info_log("*Ending Program.*")
        if (exception is not None):
            raise exception

