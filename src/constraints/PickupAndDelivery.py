import numpy
import random
import copy

from src import exceptions
from src.constraints.Constraint import Constraint


class PickupAndDelivery(Constraint):

    def __init__(self):
        super().__init__("Pickup and Delivery Constraint")
        self.max_demand = None
        self.min_demand = None
        self.pair_by_route_per = None
        self.pair_by_radius_per = None
        self.radius_limiter = None
        self.pair_by_random_per = None
        self.forbid_randomize_points_lefts = False
        self.allow_repetition = None


        # must be setted dynamically
        self.points = None
        self.cvrp_routes = None
        self.distance_matrix = None


    def get_pairs_by_route(self, has_pd):
        pickup_and_deliveries = []
        
        for route in self.cvrp_routes:
            items_to_remove = set()
            for item in route:
                if (random.randint(1,100) > self.pair_by_route_per):
                    items_to_remove.add(item)
            
            route -= items_to_remove

            route_pairs = []

            while (len(route) > 1):
                pair = random.sample(route, 2)
                if (not self.allow_repetition):
                    if (has_pd[pair[0]]):
                        route.remove(pair[0])
                        continue

                    if (has_pd[pair[1]]):
                        route.remove(pair[1])
                        continue
                
                
                route.remove(pair[0])
                route.remove(pair[1])

                pair = tuple(pair)
                route_pairs.append(pair)

                has_pd[pair[0]] = True
                has_pd[pair[1]] = True

            pickup_and_deliveries += route_pairs

        return pickup_and_deliveries


    def get_pairs_by_radious(self, has_pd):
        pickups_and_deliveries = []
        already_chosen = set()

        if (not self.allow_repetition):
            indices_with_pd = set(
                [i if has_pd[i] else None for i in range(len(self.points))]
            )

            indices_with_pd.discard(None)
            
            already_chosen = already_chosen.union(indices_with_pd)

        for i in range(len(self.points)):
            if (i in already_chosen):
                continue
            
            already_chosen.add(i)

            if (random.randint(1,100) > self.pair_by_radius_per):
                continue

            indices = set(
                numpy.where(
                    self.distance_matrix[i] < self.radius_limiter
                )[0]
            )
            
            indices -= already_chosen

            if (len(indices) < 1):
                continue

            j = random.sample(indices, 1)[0]
            already_chosen.add(j)
            while (
                len(already_chosen) < len(indices)
                and random.randint(1,100) > self.pair_by_radius_per
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

            pickups_and_deliveries.append(pair)
        
        return pickups_and_deliveries


    def get_pairs_by_random(self, has_pd, ignore_perability=False):
        pickup_and_deliveries = []
    
        indices = [x for x in range(len(self.points))]
        indices = set(indices)

        if (not self.allow_repetition):
            indices_with_pd = set(
                [i if has_pd[i] else None for i in range(len(self.points))]
            )
            indices_with_pd.discard(None)
        
            indices -= indices_with_pd

        while (len(indices) > 1):
            i = random.sample(indices, 1)[0]
            indices.remove(i)
            if (not ignore_perability):
                if (random.randint(1,100) > self.pair_by_random_per):
                    continue
                
            if (has_pd[i] and not self.allow_repetition):
                continue
            
            j = random.sample(indices, 1)[0]
            indices.remove(j)
            
            if (has_pd[j] and not self.allow_repetition):
                continue

            if (not ignore_perability):
                while (
                    len(indices) > 0 
                    and random.randint(1,100) > self.pair_by_random_per
                ):
                    j = random.sample(indices, 1)[0]
                    indices.remove(j)
                    if (has_pd[j] and not self.allow_repetition):
                        continue
            
            pair = (i, j)
            
            has_pd[i] = True
            has_pd[j] = True

            pickup_and_deliveries.append(pair)
            
        return pickup_and_deliveries


    def get_demands(self, pickup_and_deliveries):
        demands = {}

        for pair in pickup_and_deliveries:
            pickup, delivery = pair

            demand = random.randint(self.min_demand, self.max_demand)

            demands[pickup] = demand
            demands[delivery] = demand

        return demands


    def remove_points_without_requests(self, pickups_and_deliveries):
        pickups = set([i for i, j in pickups_and_deliveries])
        deliveries = set([j for i, j in pickups_and_deliveries])

        maintained_indices = []
        removed_indices = []

        for i in range(len(self.points)):
            if (i not in pickups and i not in deliveries):
                removed_indices.append(i)
                continue
            maintained_indices.append(i)

        self.points = [self.points[i] for i in maintained_indices]

        for i in removed_indices:
            for index, pd in enumerate(pickups_and_deliveries):
                pickup, delivery = pd
                if (pickup > i):
                    pickup -= 1
                if (delivery > i):
                    delivery -= 1
                pickups_and_deliveries[index] = (pickup, delivery)


    def get_constraint(self):
        self.validate_values()

        has_pd = [False for i in range(len(self.points))]

        pairs_by_routes = self.get_pairs_by_route(has_pd=has_pd)
        pairs_by_radious = self.get_pairs_by_radious(has_pd=has_pd)
        pairs_by_random = self.get_pairs_by_random(has_pd=has_pd)

        lefts_pairs = []
        if (not self.forbid_randomize_points_lefts):
            lefts_pairs = (
                self.get_pairs_by_random(has_pd=has_pd, ignore_perability=True)
            )

        pickup_and_deliveries = (
            pairs_by_routes 
            + pairs_by_radious 
            + pairs_by_random
            + lefts_pairs
        )
        
        self.remove_points_without_requests(pickup_and_deliveries)

        demands = self.get_demands(pickup_and_deliveries)

        return {
            "demands": demands, 
            "pickups_and_deliveries": pickup_and_deliveries
        }


    def get_dynamic_setting_elements(self):
        pd_attributes_to_problem = {
            "points" : "points",
            "cvrp_routes" : "cvrp_routes",
            "distance_matrix" : "distance_matrix"
        }
        
        return pd_attributes_to_problem


    def validate_values(self):
        if (self.points is None):
            raise exceptions.ParamMustBeSetted("PickupAndDelivery.points")

        if (self.cvrp_routes is None and self.pair_by_route_per > 0):
            raise exceptions.ParamMustBeSetted("PickupAndDelivery.cvrp_routes")

        if (self.distance_matrix is None and self.pair_by_radius_per > 0):
            raise exceptions.ParamMustBeSetted(
                "PickupAndDelivery.distance_matrix"
            )

        if (self.min_demand is None and self.max_demand is None):
            raise exceptions.MinOrMaxGreaterThanZero(
                "PickupAndDelivery.min_demand", 
                "PickupAndDelivery.max_demand"
            )

        if (self.min_demand <= 0 and self.max_demand <= 0):
            raise exceptions.MinOrMaxGreaterThanZero(
                "PickupAndDelivery.min_demand", 
                "PickupAndDelivery.max_demand"
            )

        if (self.min_demand is None):
            self.min_demand = self.max_demand
        
        if (self.max_demand is None):
            self.max_demand = self.min_demand

        if (self.min_demand is not None):
            if (self.max_demand < self.min_demand):
                raise exceptions.MaxMustBeGreaterThanMin(
                    "PickupAndDelivery.min_demand", 
                    "PickupAndDelivery.max_demand"
                )

            if (self.min_demand < 0):
                raise exceptions.ValueCannotBeNoneNegative(
                    "PickupAndDelivery.min_demand"
                )

        if (self.pair_by_route_per is None):
            self.pair_by_route_per = 0
        
        if (self.pair_by_radius_per is None):
            self.pair_by_radius_per = 0
        
        if (self.pair_by_random_per is None):
            self.pair_by_random_per = 0
        
        if (self.allow_repetition is None):
            self.allow_repetition = False

        if (self.pair_by_radius_per > 0):
            if (self.radius_limiter is None or self.radius_limiter <= 0):
                raise exceptions.GreaterThanZeroParameter(
                    "PickupAndDelivery.radius_limiter"
                )
    
        if (self.forbid_randomize_points_lefts is None):
            self.forbid_randomize_points_lefts = False
    

