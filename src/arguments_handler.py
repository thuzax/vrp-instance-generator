import argparse
import json

from src import constraints
from src import points_generation_managers
from src import input_filters
from src import problems
from src import matrices_calculation
from src import subproblems

from src.problems import *
from src.points_generation_managers import *


def create_problem_class(problem_class_dict):
    problem_class_name = list(problem_class_dict.keys())[0]
    
    problem_class_type = getattr(
        problems, 
        problem_class_name
    )

    problem_class = problem_class_type()
    for attribute, value in problem_class_dict[problem_class_name].items():
        problem_class.set_attribute(attribute, value)


def create_points_generator(points_generator_dict):
    points_gen_name = list(points_generator_dict.keys())[0]
    
    points_generator_type = getattr(
        points_generation_managers, 
        points_gen_name
    )

    points_generator = points_generator_type()
    for attribute, value in points_generator_dict[points_gen_name].items():
        points_generator.set_attribute(attribute, value)


def create_filters(filters_dict):
    filters_list = []
    points_generator = PointsGeneratorManager()

    if (filters_dict is None):
        points_generator.set_attribute("filters", [])
        return
    
    for filter_class_name, attributes in filters_dict.items():
        filter_class_type = getattr(input_filters, filter_class_name)
        filter_object = filter_class_type()
        filters_list.append(filter_object)

        for attribute, value in attributes.items():
            filter_object.set_attribute(attribute, value)
    
    points_generator.set_attribute("filters", filters_list)



def create_input_objects(dict_input):

    problem_class_dict = dict_input["problem_class"]
    create_problem_class(problem_class_dict)

    points_generator_dict = dict_input["points_generator"]
    create_points_generator(points_generator_dict)
    
    filters_dict = dict_input.get("filters")
    create_filters(filters_dict)
    

def create_matrices_calculator(dict_mat_calculations):

    matrices_calculator_name = list(dict_mat_calculations.keys())[0]
    matrices_calculator_dict = dict_mat_calculations[matrices_calculator_name]
    matrices_calculator_type = getattr(
        matrices_calculation,
        matrices_calculator_name
    )

    matrices_calculator_class = matrices_calculator_type()
    for attribute, value in matrices_calculator_dict.items():
        matrices_calculator_class.set_attribute(attribute, value)

    problem_class = ProblemClass()
    matrices_calculator_class.set_log_file(
        problem_class.output_path,
        problem_class.output_name
    )


def create_subproblems(dict_subproblems):
    subproblems_list = []
    for class_name, attributes in dict_subproblems.items():
        class_type = getattr(subproblems, class_name)
        subproblem_object = class_type()
        if (subproblem_object not in subproblems_list):
            subproblems_list.append(subproblem_object)

        for attribute, value in attributes.items():
            subproblem_object.set_attribute(attribute, value)

    problem_class = ProblemClass()
    problem_class.set_attribute("subproblems", subproblems_list)


def create_constraints_objects(dict_cons_class):
    constraints_to_generate = {}
    for class_name, attributes in dict_cons_class.items():
        class_type = getattr(constraints, class_name)
        constraint_object = class_type()
        constraints_to_generate[class_name] = constraint_object

        for attribute, value in attributes.items():

            if (attribute != "subproblems"):
                constraint_object.set_attribute(attribute, value)
                continue
            
            constraint_object.subproblems = []
            subproblems_dict = value
    
            for subprob_name, subprob_attrs in subproblems_dict.items():
                subproblem_type = getattr(subproblems, subprob_name)
                subproblem_instance = subproblem_type()
    
                for attribute, value in subprob_attrs.items():
                    subproblem_instance.set_attribute(attribute, value)
                
                constraint_object.subproblems.append(subproblem_instance)
    
    problem_class = ProblemClass()
    problem_class.set_attribute("constraints_objects", constraints_to_generate)



def read_configurations(arguments):
    constraints_file_name = arguments["configuration_file"]

    with open(constraints_file_name, "r") as config_file:
        text = config_file.read()
        dict_data = json.loads(text)

        dict_input = dict_data["input"]
        create_input_objects(dict_input)
        
        dict_matrices_calculations = dict_data["matrices_calculations"]
        create_matrices_calculator(dict_matrices_calculations)

        dict_subproblems = dict_data["subproblems"]
        create_subproblems(dict_subproblems)

        dict_cons_class = dict_data["constraints"]
        create_constraints_objects(dict_cons_class)



def parse_command_line_arguments():
    """Manage the command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--set-config-file",
        dest="configuration_file",
        help="parameter configuration json file to be used. The file will have priority over the command line arguments if there conflicts in parameters",
        action="store",
        default=None,
        required=True
    )

    parser.add_argument(
        "--set-seed",
        dest="seed",
        help="set the random function seed.",
        action="store",
        default=None,
        type=int,
        required=False
    )

    args = parser.parse_args()

    arguments = vars(args)

    return arguments

