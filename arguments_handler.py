import argparse

import global_parameters

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


    args = parser.parse_args()


    arguments = vars(args)

    for key, value in arguments.items():
        global_parameters.set_parameter(key, value)