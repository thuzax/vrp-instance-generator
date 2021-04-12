import numpy
import random
import copy
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
    distance_matrix = numpy.array(distance_matrix)
    time_matrix = numpy.array(time_matrix)
    execution_log.info_log("Done.")

    return (distance_matrix, time_matrix)

def generate_cvrp_capacity():
    execution_log.info_log("Generating CVRP capacity...")

    # capacity = random.randint(1,20) * 10
    capacity = 1000000000

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


def generate_pickups_and_deliveries_by_routes(routes):
    pairs_pick_deli = []
    for route in routes:
        copy_route = copy.copy(route)

        route_pairs = []

        while (len(route) > 1):
            pair = random.sample(route, 2)
            route.remove(pair[0])
            route.remove(pair[1])

            pair = tuple(pair)

            route_pairs.append(pair)

        if (len(route) == 1):
            node = routes.pop()
            copy_route.remove(node)
            
            pair = [node, random.sample(copy_route, 1)[0]]
            random.shuffle(pair)
            pair = tuple(pair)

            route_pairs.append(pair)
        
        pairs_pick_deli += route_pairs

    return pairs_pick_deli


def generate_pickups_and_deliveries_by_distance(distance_pd, distance_matrix):
    pairs = []
    already_chosen = set()

    for i in range(len(distance_matrix)):
        if (i in already_chosen):
            continue
        
        already_chosen.add(i)

        indexes = set(numpy.where(distance_matrix[i] < distance_pd)[0])
        indexes -= already_chosen

        if (len(indexes) < 1):
            continue

        j = random.sample(indexes, 1)[0]
        already_chosen.add(j)

        pair = [i, j]
        random.shuffle(pair)
        pair = tuple(pair)


        pairs.append(pair)
    
    return pairs

def generate_pickups_and_deliveries_randomly(output_size):
    pairs = []
    
    indexes = [x for x in range(output_size)]
    random.shuffle(indexes)
    indexes = set(indexes)

    while (len(indexes) > 1):
        i, j = tuple(random.sample(indexes, 2))

        indexes.remove(i)
        indexes.remove(j)
        
        pair = (i, j)
        pairs.append(pair)
    
    return pairs
