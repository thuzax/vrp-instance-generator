import global_parameters
import arguments_handler
import csv_manager
import filter_csv

def draw_elements(data, output_size):
    if (len(data) < output_size):
        return data

    data = data.sample(n=output_size)

    return data

if __name__=="__main__":
    global_parameters.init()
    arguments_handler.parse_command_line_arguments()
    
    # read input
    data = csv_manager.read_input_file()
    # filter data
    data = filter_csv.filter_data(data)

    parameters = global_parameters.get_global_parameters_names()

    par_output_size = parameters[12]
    par_output_name = parameters[13]

    output_size = global_parameters.get_parameter(par_output_size)
    output_name = global_parameters.get_parameter(par_output_name)

    # choose the random address/points
    data = draw_elements(data, output_size)

    # write data
    csv_manager.write_output_file(data, output_name)
