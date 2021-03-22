from src import global_parameters
from src import arguments_handler
from src import csv_manager
from src import filter_csv
from src import generation_manager
from src import cvrp_file_manager



if __name__=="__main__":
    global_parameters.init()
    arguments_handler.parse_command_line_arguments()
    arguments_handler.read_configuration_file()
    
    # read input
    data = csv_manager.read_input_file()
    
    # filter data
    data = filter_csv.filter_data(data)


    # choose the random address/points
    data = generation_manager.draw_instance_elements(data)

    points = csv_manager.get_points_coordinates(data)
    
    output_name = global_parameters.output_name()
    output_size = global_parameters.output_size()

    # write data in csv file
    csv_manager.write_output_file(data, output_name)

    distance_matrix, time_matrix = generation_manager.calculate_matrices(points)
    # print(distance_matrix)
    # print(time_matrix)

    
    cvrp_file_name = output_name.split("/")[-1].split(".")[0] + ".vrp"
    cvrp_file_name = "/".join(output_name.split("/")[:-1]) + "/" + cvrp_file_name

    cvrp_capacity = generation_manager.generate_cvrp_capacity()
    cvrp_demands = generation_manager.generate_cvrp_demands(output_size)


    cvrp_file_manager.write_file(
                        cvrp_file_name,
                        output_size, 
                        cvrp_capacity, 
                        points, 
                        cvrp_demands
                    )

    