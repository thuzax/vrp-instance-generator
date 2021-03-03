import argparse

import global_parameters
import exceptions

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
        required=True
    )

    # Name of output file
    parser.add_argument(
        "--output-name", 
        dest="output_name",
        help="name of the CSV output file",
        action="store",
        default=None,
        required=True
    )


    # Number of rows for the output
    parser.add_argument(
        "--output-size", 
        dest="output_size",
        help="desired number of elements in the CSV output file",
        action="store",
        default=None,
        required=True
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
        help="forbid two or more entries for the same point. If there are repetition, maintain the first found entrie",
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

    # If --use-number-column was not specified but arguments which depends
    # on it were, an exception is raised
    if (arguments["number_column_name"] is None):
        if (arguments["block_no_number"]):
            raise exceptions.ParamUsedButNoParamRequired(
                                "--block-no-number", 
                                "--use-number-column"
                            )

    # If --use-street-name was not specified but arguments which depends
    # on it were, an exception is raised
    if (arguments["number_column_name"] is None):
        if (arguments["block_no_street"]):
            raise exceptions.ParamUsedButNoParamRequired(
                                "--block-no-street", 
                                "--use-street-name"
                            )

    # print(arguments)

    for key, value in arguments.items():
        global_parameters.set_parameter(key, value)
