import argparse

import global_parameters
import exceptions

def parse_command_line_arguments():
    """Manage the command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--instance-name", 
        help="name of the input CSV file",
        action="store", 
        default=None,
        required=True
    )

    parser.add_argument(
        "-lat-col", 
        "--latitude-column-name", 
        help="name of the latitude column of the CSV input instance",
        action="store", 
        default="lat",
        required=False
    )

    parser.add_argument(
        "-lon-col",
        "--longitude-column-name", 
        help="name of the longitude column of the CSV input instance",
        action="store",
        default="lon",
        required=False
    )

    parser.add_argument(
        "-l",
        "--limits",
        help="add a box to limit the factible map area. If used, makes mandatory the following -min-lat; -max-lat; -min-lon; -max-lon",
        action="store_true",
        default=False,
        required=False
    )

    parser.add_argument(
        "-min-lat",
        "--min-latitude",
        help="limits the factible points minumum latitude of the input map",
        action="store",
        default=None,
        required=False
    )

    parser.add_argument(
        "-max-lat",
        "--max-latitude",
        help="limits the factible points maximum latitude of the input map",
        action="store",
        default=None,
        required=False
    )

    parser.add_argument(
        "-min-lon",
        "--min-longitude",
        help="limits the factible points minumum longitude of the input map",
        action="store",
        default=None,
        required=False
    )

    parser.add_argument(
        "-max-lon",
        "--max-longitude",
        help="limits the factible points maximum longitude of the input map",
        action="store",
        default=None,
        required=False
    )

    args = parser.parse_args()

    arguments = vars(args)

    # print(arguments)

    limits = [
            arguments["min_latitude"], 
            arguments["max_latitude"], 
            arguments["min_longitude"], 
            arguments["max_longitude"]
        ]


    if (arguments["limits"] and (not any(limits))):
        raise exceptions.ParamLimitNotSpecified()
    
    if (any(limits) and (not arguments["limits"])):
        raise exceptions.ParamLimitSpecifiedWithoutParamLimits
    

    for key, value in arguments.items():
        global_parameters.set_parameter(key, value)