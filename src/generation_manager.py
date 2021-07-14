import math
import numpy
import random
import copy
import collections
from numpy.core.defchararray import center
import scipy.spatial
import sklearn.cluster
import matplotlib.pyplot
from progress.bar import Bar
# from sklearn.externals.six import remove_move


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
    # distance_matrix *= 1000
    distance_matrix = numpy.around(distance_matrix)
    time_matrix = numpy.array(time_matrix)
    time_matrix = numpy.around(time_matrix)
    
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


def generate_pickups_and_deliveries_by_routes(routes, has_pd):
    pairs_pick_deli = []
    pick_deli_probability = global_parameters.pick_deli_by_route_per()
    repeat_pd_only_if_needed = global_parameters.repeat_pd_only_if_needed()
    no_repeat_pd = global_parameters.no_repeat_pd()

    for route in routes:
        items_to_remove = set()
        for item in route:
            if (random.randint(1,100) > pick_deli_probability):
                items_to_remove.add(item)
        
        route -= items_to_remove

        copy_route = copy.copy(route)
        route_pairs = []

        while (len(route) > 1):
            pair = random.sample(route, 2)
            if (
                (repeat_pd_only_if_needed or no_repeat_pd)
                and (has_pd[pair[0]] or has_pd[pair[1]])
            ):
                if (has_pd[pair[0]]):
                    route.remove(pair[0])
                
                if (has_pd[pair[1]]):
                    route.remove(pair[1])
                
                continue

            route.remove(pair[0])
            route.remove(pair[1])


            pair = tuple(pair)
            route_pairs.append(pair)

            has_pd[pair[0]] = True
            has_pd[pair[1]] = True
        
        if (len(route) == 1 and len(copy_route) > 1 and (not no_repeat_pd)):
            node = route.pop()
            
            second_node = random.sample(copy_route, 1)[0]
            while (second_node == node):
                second_node = random.sample(copy_route, 1)[0]
                continue

            pair = [node, second_node]
            random.shuffle(pair)
            pair = tuple(pair)

            route_pairs.append(pair)
            
            has_pd[pair[0]] = True
            has_pd[pair[1]] = True

        pairs_pick_deli += route_pairs

    return pairs_pick_deli


def generate_pickups_and_deliveries_by_dist(
    distance_pd, 
    distance_matrix, 
    has_pd
):
    pairs = []
    already_chosen = set()

    no_repeat_pd = global_parameters.no_repeat_pd() 
    repeat_pd_only_if_needed = global_parameters.repeat_pd_only_if_needed()

    if (no_repeat_pd or repeat_pd_only_if_needed):
        indices_with_pd = set(
            [i if has_pd[i] else None for i in range(len(distance_matrix))]
        )
        indices_with_pd.remove(None)
        
        already_chosen = already_chosen.union(indices_with_pd)

    pick_deli_probability = global_parameters.pick_deli_by_distance_per()

    for i in range(len(distance_matrix)):
        if (i in already_chosen):
            continue
        
        already_chosen.add(i)

        if (random.randint(1,100) > pick_deli_probability):
            continue

        indices = set(numpy.where(distance_matrix[i] < distance_pd)[0])
        indices -= already_chosen

        if (len(indices) < 1):
            continue

        j = random.sample(indices, 1)[0]
        already_chosen.add(j)
        while (
            len(already_chosen) < len(indices)
            and random.randint(1,100) > pick_deli_probability
        ):
            j = random.sample(indices, 1)[0]
            already_chosen.add(j)
        
        if (len(already_chosen) == len(indices)):
            continue

        pair = [i, j]
        random.shuffle(pair)
        pair = tuple(pair)

        has_pd[pair[0]] = True
        has_pd[pair[1]] = True

        pairs.append(pair)
    
    return pairs

def generate_pickups_and_deliveries_randomly(output_size, has_pd):
    pairs = []
    
    indices = [x for x in range(output_size)]
    indices = set(indices)

    pick_deli_probability = global_parameters.pick_deli_random_per()
    no_repeat_pd = global_parameters.no_repeat_pd()
    repeat_pd_only_if_needed = global_parameters.repeat_pd_only_if_needed()

    if (no_repeat_pd or repeat_pd_only_if_needed):
        indices_with_pd = set(
            [i if has_pd[i] else None for i in range(output_size)]
        )
        indices_with_pd.remove(None)
    
        indices -= indices_with_pd

    while (len(indices) > 1):
        i = random.sample(indices, 1)[0]
        indices.remove(i)
        if (random.randint(1,100) > pick_deli_probability):
            continue
        
        if (has_pd[i] and (no_repeat_pd or repeat_pd_only_if_needed)):
            continue
        
        j = random.sample(indices, 1)[0]
        indices.remove(j)
        
        while (
            len(indices) > 0 
            and random.randint(1,100) > pick_deli_probability
        ):
            j = random.sample(indices, 1)[0]
            indices.remove(j)
            if (has_pd[j] and (no_repeat_pd or repeat_pd_only_if_needed)):
                continue
        
        pair = (i, j)
        pairs.append(pair)
        has_pd[i] = True
        has_pd[j] = True

    
    return pairs

def generate_pickups_and_deliveries(
    routes=None, 
    distance_matrix=None, 
    output_size=None
):

    has_pd = [False for i in range(len(distance_matrix))]

    route_pd = generate_pickups_and_deliveries_by_routes(
                                routes,
                                has_pd
                            )

    distance_pd = global_parameters.max_distance_pd()
    dist_pd = generate_pickups_and_deliveries_by_dist(
                                    distance_pd,
                                    distance_matrix,
                                    has_pd
                                )

    rand_pd = generate_pickups_and_deliveries_randomly(
                                    output_size,
                                    has_pd
                                )

    pickups_and_deliveries = route_pd + dist_pd + rand_pd

    pickups = set([pickup for pickup, delivery in pickups_and_deliveries])
    deliveries = set([delivery for pickup, delivery in pickups_and_deliveries])

    chosen = pickups.union(deliveries)

    possible_indices = set([i for i in range(output_size)]) - chosen

    # Force at least one pickup or delivery for each point
    if (
        global_parameters.no_repeat_pd() 
        or global_parameters.repeat_pd_only_if_needed()
    ):

        while (len(possible_indices) > 1):
            i = possible_indices.pop()
            
            j = random.sample(possible_indices, 1)[0]

            possible_indices.remove(j)

            pair = [i, j]
            random.shuffle(pair)
            pair = tuple(pair)
            
            pickups_and_deliveries.append(pair)
            pickups.add(pair[0])
            deliveries.add(pair[1])

            has_pd[pair[0]] = True
            has_pd[pair[1]] = True

        if (len(possible_indices) == 1):
            if (global_parameters.no_repeat_pd()):
                element = possible_indices.pop()
                text = ""
                text += "The element <" 
                text += str(element) 
                text += "> will not have a pair. " 
                text += "Even output size with no repetitions."
                execution_log.warning_log(text)
            else:
                i = possible_indices.pop()
                
                j = random.sample(
                            (
                                set([k for k in range(output_size)]) 
                                - set([i])
                            ), 
                            1
                        )[0]

                pair = [i, j]
                random.shuffle(pair)
                pair = tuple(pair)
                
                pickups_and_deliveries.append(pair)
                pickups.add(pair[0])
                deliveries.add(pair[1])

                has_pd[pair[0]] = True
                has_pd[pair[1]] = True
            
                text = ""
                text += "The element <" 
                text += str(j) 
                text += "> was repeated as a pair of element <" 
                text += str(i)
                text += ">."
                execution_log.warning_log(text)


    else:
        for i in range(output_size):
            if (i in pickups):
                continue
            if i in deliveries:
                continue
            
            j = random.randint(0,output_size-1)
            while (i == j):
                j = random.randint(0,output_size-1)
            pair = [i, j]
            random.shuffle(pair)
            pair = tuple(pair)
            
            pickups_and_deliveries.append(pair)
            pickups.add(pair[0])
            deliveries.add(pair[1])

            has_pd[pair[0]] = True
            has_pd[pair[1]] = True

    return pickups_and_deliveries




def duplicate_pick_and_deli_points(pickups_and_deliveries, points):
    numbers_of_picks = numpy.zeros(len(points))
    numbers_of_delis = numpy.zeros(len(points))
    
    pickups_dests = {}
    delis_origs = {}

    for pickup, delivery in pickups_and_deliveries:
        
        numbers_of_picks[pickup] += 1
        numbers_of_delis[delivery] += 1
        

    pickups = []
    deliveries = []


    pickups_index_relations = {}
    deliveries_index_relations = {}

    for i in range(len(points)):
        
        if (numbers_of_picks[i] > 0):
            pickups_index_relations[i] = len(pickups)
            pickups.append(copy.deepcopy(points[i]))

        if (numbers_of_delis[i] > 0):
            deliveries_index_relations[i] = len(deliveries)
            deliveries.append(copy.deepcopy(points[i]))

    for pickup, delivery in pickups_and_deliveries:

            pickup_equivalent_index = pickups_index_relations[pickup]

            p = pickups_dests.get(pickup_equivalent_index)
            delivery_equivalent_index = deliveries_index_relations[delivery]
            if (p is None):
                pickups_dests[pickup_equivalent_index] = set()
            
            pickups_dests[pickup_equivalent_index].add(
                                                    delivery_equivalent_index
                                                )

            
            d = delis_origs.get(delivery_equivalent_index)
            if (d is None):
                delis_origs[delivery_equivalent_index] = set()
            
            delis_origs[delivery_equivalent_index].add(
                                                    pickup_equivalent_index
                                                )

    return pickups, deliveries, pickups_dests, delis_origs


def remove_points_without_request(points, pickups_and_deliveries):
    pickups = set([i for i, j in pickups_and_deliveries])
    deliveries = set([j for i, j in pickups_and_deliveries])

    maintained_indices = []
    removed_indices = []

    for i in range(len(points)):
        if (i not in pickups and i not in deliveries):
            removed_indices.append(i)
            continue
        maintained_indices.append(i)

    points = [points[i] for i in maintained_indices]

    for i in removed_indices:
        for index, pd in enumerate(pickups_and_deliveries):
            pickup, delivery = pd
            if (pickup > i):
                pickup -= 1
            if (delivery > i):
                delivery -= 1
            pickups_and_deliveries[index] = (pickup, delivery)

    return points, pickups_and_deliveries
    

def generate_time_windows(
        pickups_and_deliveries,
        points,
        services_times,
        time_matrix
):
    """Generate time windows for pickups and deliveries
    """

    if (not global_parameters.generate_time_windows()):
        return None
    
    execution_log.info_log("Generating time windows...")



    tw_size = global_parameters.time_windows_size()
    tw_horizon = global_parameters.time_windows_horizon()

    time_windows = {}

    bar = Bar(
            "Calculating:", 
            max=len(pickups_and_deliveries),
            suffix='%(percent)d%%'
        )

    for pickup, delivery in pickups_and_deliveries:
        
        # Calculate pickup time window
        ## calculate interval for a central point
        tw_pickup_interval_start = math.ceil(tw_size / 2)
        tw_pickup_interval_end = (
                tw_horizon 
                - time_matrix[pickup][delivery]
                - services_times[pickup]
                - services_times[delivery]
                - math.ceil(tw_size / 2)
            )

        ## select a central point from interval
        pickup_central_point = random.randint(
                tw_pickup_interval_start, 
                tw_pickup_interval_end
            )
        
        ## calculate the start and end time for the window using 
        ## the central point
        tw_pickup_start = pickup_central_point - math.ceil(tw_size / 2)
        tw_pickup_end = pickup_central_point + math.ceil(tw_size / 2)

        
        time_windows_pickup = (tw_pickup_start, tw_pickup_end)

        # Calculate delivery time window
        ## calculate interval for a central point based on the pickup window
        ## since the pickup must be done before the delivery
        tw_delivery_interval_start = (
                tw_pickup_start 
                + math.ceil(tw_size / 2)
            )

        tw_delivery_interval_end = tw_pickup_interval_end

        delivery_central_point = random.randint(
                tw_delivery_interval_start,
                tw_delivery_interval_end
            )
        
        tw_delivery_start = delivery_central_point - math.ceil(tw_size / 2)
        tw_delivery_end = delivery_central_point + math.ceil(tw_size / 2)

        time_windows_delivery = (tw_delivery_start, tw_delivery_end)

        time_windows[(pickup, delivery)] = (
                time_windows_pickup, 
                time_windows_delivery
            )

        
        bar.next()

    bar.finish()

    execution_log.info_log("Done.")

    return time_windows


def generate_services_times(points):
    """Generate service times for pickups and deliveries
    """

    if (not global_parameters.generate_service_time()):
        return

    min_service_time = global_parameters.min_service_time()
    max_service_time = global_parameters.max_service_time()


    services_times = None
    if (min_service_time < 0):
        services_times = numpy.full(
                                shape=len(points), 
                                fill_value=max_service_time
                            )
    else:
        services_times = numpy.array([
                            random.randint(
                                min_service_time, 
                                max_service_time
                            ) for i in range(len(points))
                        ])
    
    return services_times


def generate_urb_rur_aptitude(points):
    method = global_parameters.generation_urb_rur_method()

    distances_to_center = None

    if (method == "clustering"):
        distances_to_center = generate_urb_rur_aptitude_by_clustering(points)

    if (method == "center_seeds"):
        distances_to_center = generate_urb_rur_aptitude_by_center_seeds(points)

    if (distances_to_center is None):
        return None

    points_classif = classify_using_distances_to_center(
                            points, 
                            distances_to_center
                        )

    for i, point in enumerate(points):
        if (points_classif[i] == "u"):
            matplotlib.pyplot.scatter(
                point[0],
                point[1],
                color="blue"
            )
        if (points_classif[i] == "r"):
            matplotlib.pyplot.scatter(
                point[0],
                point[1],
                color="red"
            )

    # matplotlib.pyplot.show()
    output_path = global_parameters.output_path()
    output_name = global_parameters.output_name()

    matplotlib.pyplot.gca().set_aspect('equal', adjustable='box')
    matplotlib.pyplot.xticks(rotation=-15)

    fig_name = output_path + "/" + "fig_" + output_name + ".png"
    matplotlib.pyplot.savefig(fig_name)

    return points_classif


def generate_urb_rur_aptitude_by_clustering(points):
    number_of_clusters = global_parameters.number_urban_centers()

    points_arr = numpy.array(points)

    kmeans = sklearn.cluster.KMeans(n_clusters=number_of_clusters)
    kmeans.fit(points_arr)
    
    matplotlib.pyplot.scatter(
        kmeans.cluster_centers_[:,0],
        kmeans.cluster_centers_[:,1],
        color="black"
    )
    for x,y in kmeans.cluster_centers_:
        matplotlib.pyplot.annotate(
            "center",
            (x,y),
            textcoords="offset points",
            xytext=(0,10),
            ha="center"
        )

    distances_to_center = scipy.spatial.distance.cdist(
                    points_arr,
                    kmeans.cluster_centers_,
                    metric="euclidean"
                )

    return distances_to_center


def generate_urb_rur_aptitude_by_center_seeds(points):
    number_of_seeds = global_parameters.number_urban_centers()

    points_set = set(points)

    center_seeds = set()

    first_point = points[random.randint(0, len(points)-1)]

    center_seeds.add(first_point)
    number_of_seeds -= 1

    points_set.remove(first_point)

    candidates_set_size = math.ceil(len(points)**(1/2))

    while(number_of_seeds > 0):
        candidates_set = random.sample(points_set, candidates_set_size)

        number_of_seeds -= 1

        candidates_arr = numpy.array(candidates_set)
        center_seeds_arr = numpy.array(list(center_seeds))


        distances = scipy.spatial.distance.cdist(
                                    candidates_arr, 
                                    center_seeds_arr,
                                    metric="euclidean"
                                )

        seed_position = numpy.argmax(numpy.amin(distances, axis=1))

        center_seeds.add(candidates_set[seed_position])
        points_set.remove(candidates_set[seed_position])

    points_arr =numpy.array(points)
    center_seeds_arr = numpy.array(list(center_seeds))


    matplotlib.pyplot.scatter(
        center_seeds_arr[:,0],
        center_seeds_arr[:,1],
        color="black"
    )
    for x,y in center_seeds_arr:
        matplotlib.pyplot.annotate(
            "center",
            (x,y),
            textcoords="offset points",
            xytext=(0,10),
            ha="center"
        )

    distances_to_center_seeds = scipy.spatial.distance.cdist(
                    points_arr,
                    center_seeds_arr,
                    metric="euclidean"
                )

    return distances_to_center_seeds


def classify_using_distances_to_center(points, distances_to_center):
    points_min_distance = numpy.amin(distances_to_center, axis=1)

    urb_rur_points = []

    for i in range(len(points)):
        if (points_min_distance[i] == 0 
            and global_parameters.generation_urb_rur_method() == "clustering"):
            urb_rur_points.append("r")
            continue
        
        if (points_min_distance[i] > global_parameters.max_urban_distance()):
            urb_rur_points.append("r")
            continue

        urb_rur_points.append("u")

    return urb_rur_points

def generate_fleets_sizes(pickup_and_deliveries):
    cvrplib_max_vertices = 30000
    cvrplib_number_of_routes = 256
    extra_vehicles_ratio = 0.01


    number_of_vehicles = math.ceil(
                cvrplib_number_of_routes 
                * (
                    (
                        2 * len(pickup_and_deliveries)
                        / cvrplib_max_vertices
                    )
                    + extra_vehicles_ratio
                )

            )
    return number_of_vehicles

def divide_fleet(fleet_size, clients_classif):
    repetitions = collections.Counter(clients_classif)

    number_urban_clients = repetitions["u"]
    number_rural_clients = repetitions["r"]

    urban_fleet_size = math.ceil(
                        (number_urban_clients / len(clients_classif))
                        * fleet_size
                    )

    rural_fleet_size = math.ceil(
                        (number_rural_clients / len(clients_classif))
                        * fleet_size
                    )

    return (urban_fleet_size, rural_fleet_size)