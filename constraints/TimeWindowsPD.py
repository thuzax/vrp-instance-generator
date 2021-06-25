import math
import random
import numpy

from src import exceptions

from constraints.Constraint import Constraint


class TimeWindowsPD(Constraint):
    def __init__(self):
        super().__init__("Time Windows (for Pickup and Delivery) Constraint")
        self.time_windows_size = None
        self.planning_horizon = None
        self.time_windows_size_max_variation = None

        # Must be setted dynamically
        self.pickups_and_deliveries = None
        self.services_times = None
        self.time_matrix = None



    def generate_time_windows(self):

        time_windows = {}

        for pickup, delivery in self.pickups_and_deliveries:
            
            # Calculate pickup time window
            ## calculate interval for a central point
            tw_pickup_interval_start = math.ceil(self.time_windows_size / 2)
            tw_pickup_interval_end = (
                    self.planning_horizon 
                    - self.time_matrix[pickup][delivery]
                    - self.services_times[pickup]
                    - self.services_times[delivery]
                    - math.ceil(self.time_windows_size / 2)
                )

            ## select a central point from interval
            pickup_central_point = random.randint(
                    tw_pickup_interval_start, 
                    tw_pickup_interval_end
                )
            
            ## calculate the start and end time for the window using 
            ## the central point
            tw_pickup_start = (
                pickup_central_point 
                - math.ceil(self.time_windows_size / 2)
            )
            tw_pickup_end = (
                pickup_central_point 
                + math.ceil(self.time_windows_size / 2)
            )

            
            time_windows_pickup = (tw_pickup_start, tw_pickup_end)

            # Calculate delivery time window
            ## calculate interval for a central point based on the pickup window
            ## since the pickup must be done before the delivery
            tw_delivery_interval_start = (
                    tw_pickup_start 
                    + math.ceil(self.time_windows_size / 2)
                )

            tw_delivery_interval_end = tw_pickup_interval_end

            delivery_central_point = random.randint(
                    tw_delivery_interval_start,
                    tw_delivery_interval_end
                )
            
            tw_delivery_start = (
                delivery_central_point 
                - math.ceil(self.time_windows_size / 2)
            )
            tw_delivery_end = (
                delivery_central_point 
                + math.ceil(self.time_windows_size / 2)
            )

            time_windows_delivery = (tw_delivery_start, tw_delivery_end)

            time_windows[(pickup, delivery)] = (
                    time_windows_pickup, 
                    time_windows_delivery
                )

        return time_windows

    def get_constraint(self):
        time_windows_pd = self.generate_time_windows()

        return {
            "time_windows_pd": time_windows_pd, 
            "planning_horizon" : self.planning_horizon,
            "time_windows_size": self.time_windows_size
        }

    def validate_values(self):
        if (self.pickups_and_deliveries is None):
            raise exceptions.ParamMustBeSetted("pickup_and_deliveries")
        
        if (self.time_matrix is None):
            raise exceptions.ParamMustBeSetted("time_matrix")

        if (self.time_windows_size is None or self.time_windows_size <= 0):
            raise exceptions.GreaterThanZeroParameter("time_windows_size")

        if (self.planning_horizon is None or self.planning_horizon <= 0):
            raise exceptions.GreaterThanZeroParameter("planning_horizon")

        if (self.time_windows_size_max_variation is None):
            self.time_windows_size_max_variation = 0

        if (self.services_times == None):
            self.services_times = numpy.zeros(
                len(self.pickups_and_deliveries) 
                * 2
            )
        
