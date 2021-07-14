import numpy
import random
import math
import collections

from src import exceptions
from constraints.Constraint import Constraint

class LimitedFleetUrbanRural(Constraint):
    def __init__(self):
        super().__init__("Limited Fleet (for Urban and Rural) Constraint")
        self.correction_value = None

        # Must be setted dynamically
        self.urban_rural_aptitude = None
        self.cvrp_routes = None
    
    def divide_fleet(self, fleet_size):
        repetitions = collections.Counter(self.urban_rural_aptitude)

        number_urban_clients = repetitions["u"]
        number_rural_clients = repetitions["r"]

        urban_fleet_size = math.ceil(
                            (number_urban_clients / 
                            len(self.urban_rural_aptitude))
                            * fleet_size
                        )

        rural_fleet_size = math.ceil(
                            (number_rural_clients / 
                            len(self.urban_rural_aptitude))
                            * fleet_size
                        )

        return {
            "urban_fleet_size": urban_fleet_size, 
            "rural_fleet_size": rural_fleet_size
        }

    def generate_fleet_size(self):
        fleet_size = math.ceil(
            len(self.cvrp_routes) 
            * self.correction_value
        )
        return fleet_size


    def get_constraint(self):
        fleet_size = self.generate_fleet_size()

        fleets_sizes = self.divide_fleet(fleet_size)

        return {"fleets_sizes": fleets_sizes}


    def validate_values(self):
        if (self.number_of_points is None or self.number_of_points == 0):
            raise exceptions.GreaterThanZeroParameter("number_of_points")

        if (self.min_service_time is None and self.max_service_time is None):
            raise exceptions.MinOrMaxGreaterThanZero(
                "min_service_time", 
                "max_service_time"
            )

        if (self.min_service_time <= 0 and self.max_service_time <= 0):
            raise exceptions.MinOrMaxGreaterThanZero(
                "min_service_time", 
                "max_service_time"
            )

        if (self.min_service_time is None):
            self.min_service_time = self.max_service_time
        
        if (self.max_service_time is None):
            self.max_service_time = self.min_service_time

        if (self.min_service_time is not None):
            if (self.max_service_time < self.min_service_time):
                raise exceptions.MaxMustBeGreaterThanMin(
                    "min_service_time", 
                    "max_service_time"
                )

            if (self.min_service_time < 0):
                raise exceptions.ValueCannotBeNoneNegative("min_service_time")
