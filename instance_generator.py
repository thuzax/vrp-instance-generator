import global_parameters
import arguments_handler
import csv_manager

if __name__=="__main__":
    global_parameters.init()
    arguments_handler.parse_command_line_arguments()

    data = csv_manager.read_input_file()