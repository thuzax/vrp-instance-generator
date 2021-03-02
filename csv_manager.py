import global_parameters
import pandas

def read_input_file():
    """Read a CSV input file
    """
    input_instance, lat_col, lon_col = (
            global_parameters.get_global_parameters_names()
        )

    # data_frame = pandas.read_csv()