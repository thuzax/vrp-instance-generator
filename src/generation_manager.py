import numpy
from progress.bar import Bar


from src import global_parameters
from src import calculate_distances_osrm as calculate_distances
from src import exceptions
from src import execution_log


def draw_elements(data, output_size):
    """Select <output_size> random elements from the filtered input instance providaded
    """

    if (len(data) < output_size):
        return data

    data = data.sample(n=output_size)

    return data



def calculate_matrices(data):
    """Return two NxN matrices representing (respectively) the time and distance matrix.
    """


    distance_matrix = []
    time_matrix = []

    parameters = global_parameters.get_global_parameters_names()
    lat_column_name = global_parameters.get_parameter(parameters[1])
    lon_column_name = global_parameters.get_parameter(parameters[2])

    points_list = []

    for ind, row in data.iterrows():
        latitude = row[lat_column_name]
        longitude = row[lon_column_name]

        point = (
            float(latitude), 
            float(longitude)
        )

        points_list.append(point)

    execution_log.info_log("Calculating matrices...")
    bar = Bar("", max=len(data),suffix='%(percent)d%%')

    for i in range(len(points_list)):
        results = calculate_distances.request_dist_and_time_from_source(
                                            i, 
                                            points_list
                                        )

        distances, times = results

        if (distances is None or times is None):
            raise exceptions.DistanceToPointCannotBeCalculated(points_list[i])

        distance_matrix.append(distances)
        time_matrix.append(times)
        bar.next()

    bar.finish()
    numpy.array(distance_matrix)
    numpy.array(time_matrix)
    execution_log.info_log("Done.")

    return (distance_matrix, time_matrix)