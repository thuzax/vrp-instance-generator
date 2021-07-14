import argparse
import json
from importlib import import_module

import constraints
import points_generation_managers
import input_filters
import problems

from src import global_parameters
from src import exceptions


def create_input_objects(dict_input):
    problem_class_dict = dict_input["problem_class"]
    problem_class_name = list(problem_class_dict.keys())[0]
    
    problem_class_type = getattr(
        problems, 
        problem_class_name
    )

    problem_class = problem_class_type()

    for attribute, value in problem_class_dict[problem_class_name].items():
        problem_class.set_attribute(attribute, value)

    points_generator_dict = dict_input["points_generator"]

    points_gen_name = list(points_generator_dict.keys())[0]

    points_generator_type = getattr(
        points_generation_managers, 
        points_gen_name
    )

    points_generator = points_generator_type()

    for attribute, value in points_generator_dict[points_gen_name].items():
        points_generator.set_attribute(attribute, value)


    filters_dict = dict_input.get("filters")

    filters_list = []

    if (filters_dict is not None):
        for filter_class_name, attributes in filters_dict.items():
            filter_class_type = getattr(input_filters, filter_class_name)
            filter_object = filter_class_type()
            filters_list.append(filter_object)

            for attribute, value in attributes.items():
                filter_object.set_attribute(attribute, value)
        
        points_generator.set_attribute("filters", filters_list)

    else:
        points_generator.set_attribute("filters", [])



def create_constraints_objects(dict_cons_class):
    constraints_to_generate = {}
    for class_name, attributes in dict_cons_class.items():
        class_type = getattr(constraints, class_name)
        constraint_object = class_type()
        constraints_to_generate[class_name] = constraint_object

        for attribute, value in attributes.items():
            constraint_object.set_attribute(attribute, value)
    
    return constraints_to_generate


def read_configurations():
    constraints_file_name = global_parameters.constraints_config()

    with open(constraints_file_name, "r") as config_file:
        text = config_file.read()
        dict_data = json.loads(text)

        dict_input = dict_data["input"]
        create_input_objects(dict_input)


        dict_cons_class = dict_data["constraints"]
        constraints_to_generate = create_constraints_objects(dict_cons_class)
        
    
    global_parameters.set_parameter(
                        "constraints_objects", 
                        constraints_to_generate
                    )



def read_configuration_file():
    """Read the configuration file and reset the parameters values described in the file
    """
    
    configuration_file_name = global_parameters.config_file()


    if (configuration_file_name == None):
        return

    with open(configuration_file_name, "r") as config_file:
        text = config_file.read()
        dict_config = json.loads(text)

        for key, value in dict_config.items():
            key = key.lower()
            if (key == "config_file"):
                continue
            
            global_parameters.set_parameter(key, value)

    check_parameters()


def read_paths_file():
    """Read the paths file which contains the path for external programs
    """

    paths_file_name = global_parameters.paths_file()

    with open(paths_file_name, "r") as paths_file:
        text = paths_file.read()
        dict_paths = json.loads(text)

        for key, value in dict_paths.items():
            key = key.lower()

            key += "_path"
            global_parameters.set_parameter(key, value)


def parse_command_line_arguments():
    """Manage the command line arguments
    """
    parser = argparse.ArgumentParser()

    # Name of input instance
    parser.add_argument(
        "--instance-name", 
        dest="instance_name",
        help="name of the input CSV file",
        action="store", 
        default=None,
        required=False
    )

    # Name of output file
    parser.add_argument(
        "--output-name", 
        dest="output_name",
        help="name of the CSV output file",
        action="store",
        default=None,
        required=False
    )


    # Number of rows for the output
    parser.add_argument(
        "--output-size", 
        dest="output_size",
        help="desired number of elements in the CSV output file",
        action="store",
        default=None,
        required=False
    )


    #### Name of columns
    parser.add_argument(
        "--lat-col", 
        dest="lat_column_name",
        help="name of the latitude column of the CSV input instance",
        action="store", 
        default=["lat"],
        required=False,
        nargs="+"
    )

    parser.add_argument(
        "--lon-col",
        dest="lon_column_name",
        help="name of the longitude column of the CSV input instance",
        action="store",
        default=["lon"],
        required=False,
        nargs="+"
    )

    parser.add_argument(
        "--use-number-column",
        dest="number_column_name",
        help="specify the column with the number of the address that may be used",
        action="store",
        default=None,
        required=False,
        nargs="+"
    )

    parser.add_argument(
        "--use-street-name",
        dest="street_column_name",
        help="specify the column with the name of the street that may be used",
        action="store",
        default=None,
        required=False,
        nargs="+"
    )


    #### Limit region of the map
    parser.add_argument(
        "--min-lat",
        dest="min_lat",
        help="limits the factible points minumum latitude of the input map",
        action="store",
        default=None,
        required=False
    )

    parser.add_argument(
        "--max-lat",
        dest="max_lat",
        help="limits the factible points maximum latitude of the input map",
        action="store",
        default=None,
        required=False
    )

    parser.add_argument(
        "--min-lon",
        dest="min_lon",
        help="limits the factible points minumum longitude of the input map",
        action="store",
        default=None,
        required=False
    )

    parser.add_argument(
        "--max-lon",
        dest="max_lon",
        help="limits the factible points maximum longitude of the input map",
        action="store",
        default=None,
        required=False
    )

    #### Block entries
    parser.add_argument(
        "--block-point-repetition",
        dest="block_point_repetition",
        help="forbid two or more entries for the same point. If there are repetition, maintain the first found entry",
        action="store_true",
        default=False,
        required=False
    )

    parser.add_argument(
        "--block-no-number",
        dest="block_no_number",
        help="if set, remove entries without a number on NUMBER_COLUMN_NAME column",
        action="store_true",
        default=False,
        required=False
    )

    parser.add_argument(
        "--block-no-street",
        dest="block_no_street",
        help="if set, remove entries without street names",
        action="store_true",
        default=False,
        required=False
    )

    parser.add_argument(
        "--use-reaching-filter",
        dest="reaching_filter",
        help="remove all points that can't reach another random point",
        action="store_true",
        default=False,
        required=False
    )

    parser.add_argument(
        "--run-distances-remote",
        dest="distances_locally",
        help="if set, the distances between points will be calculated by the OSRM demo server (not recomended for big instances)",
        action="store_false",
        default=True,
        required=False
    )

    parser.add_argument(
        "--set-config-file",
        dest="config_file",
        help="parameter configuration json file to be used. The file will have priority over the command line arguments if there conflicts in parameters",
        action="store",
        default=None,
        required=False
    )

    args = parser.parse_args()


    arguments = vars(args)
    
    # Join column names with spaces
    if (len(arguments["lat_column_name"]) > 1):
        arguments["lat_column_name"] = " ".join(arguments["lat_column_name"])
    else:
        arguments["lat_column_name"] = "".join(arguments["lat_column_name"])

    if (len(arguments["lon_column_name"]) > 1):
        arguments["lon_column_name"] = " ".join(arguments["lon_column_name"])
    else:
        arguments["lon_column_name"] = "".join(arguments["lon_column_name"])
    

    if (arguments["number_column_name"] is not None):
        if (len(arguments["number_column_name"]) > 1):
            arguments["number_column_name"] = " ".join(
                                                arguments["number_column_name"]
                                            )
        else:
            arguments["number_column_name"] = "".join(
                                                arguments["number_column_name"]
                                            )
        
    if (arguments["street_column_name"] is not None):
        if (len(arguments["street_column_name"]) > 1):
            arguments["street_column_name"] = " ".join(
                                                arguments["street_column_name"]
                                            )
        else:
            arguments["street_column_name"] = "".join(
                                                arguments["street_column_name"]
                                            )

    # print(arguments)

    for key, value in arguments.items():
        global_parameters.set_parameter(key, value)
    
    check_parameters()

def check_parameters():
    # If --use-number-column was not specified but arguments which depends
    # on it were, an exception is raised
    if (global_parameters.number_column_name() is None):
        if (global_parameters.block_no_number()):
            raise exceptions.ParamUsedButNoParamRequired(
                                "--block-no-number", 
                                "--use-number-column"
                            )

    # If --use-street-name was not specified but arguments which depends
    # on it were, an exception is raised
    if (global_parameters.number_column_name() is None):
        if (global_parameters.block_no_street()):
            raise exceptions.ParamUsedButNoParamRequired(
                                "--block-no-street", 
                                "--use-street-name"
                            )

