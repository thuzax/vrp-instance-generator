import numpy
import random
from progress.bar import Bar


from src import global_parameters
from src import exceptions
from src import execution_log
from src import calculate_distances_osrm as calculate_distances


def draw_instance_elements(data):
    """Select <output_size> random elements from the filtered input instance providaded
    """

    output_size = global_parameters.output_size()

    if (len(data) < output_size):
        return data

    data = data.sample(n=output_size)

    return data



def calculate_matrices(points):
    """Return two NxN matrices representing (respectively) the time and distance matrix.
    """

    distance_matrix = []
    time_matrix = []

    execution_log.info_log("Calculating matrices...")
    bar = Bar("Calculating:", max=len(points),suffix='%(percent)d%%')

    for i in range(len(points)):
        results = calculate_distances.request_dist_and_time_from_source(
                                            i, 
                                            points
                                        )

        distances, times = results

        if (distances is None or times is None):
            raise exceptions.DistanceToPointCannotBeCalculated(points[i])

        distance_matrix.append(distances)
        time_matrix.append(times)
        bar.next()

    bar.finish()
    numpy.array(distance_matrix)
    numpy.array(time_matrix)
    execution_log.info_log("Done.")

    return (distance_matrix, time_matrix)

def generate_cvrp_capacity():
    execution_log.info_log("Generating CVRP capacity...")

    capacity = random.randint(1,20) * 10

    execution_log.info_log("Done.")
    return capacity

def generate_cvrp_demands(number_of_clientes):
    execution_log.info_log("Generating CVRP demands...")

    probabilities = [1, 0.5, 0.3, 0.2]

    demands = []

    for i in range(number_of_clientes):
        demands.append(0)
        for probability in probabilities:
            p = random.randint(0,1000)/1000.0
            if (p <= probability):
                demands[i] += 1

    execution_log.info_log("Done.")
    
    
    return demands

