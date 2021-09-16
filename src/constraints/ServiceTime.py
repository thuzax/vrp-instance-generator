import numpy
import random

from src import exceptions
from src.constraints.Constraint import Constraint

class ServiceTime(Constraint):
    def __init__(self):
        super().__init__("Service Time Constraint")
        self.max_service_time = None
        self.min_service_time = None

        # Must be setted dynamically
        self.number_of_points = None
        self.points_indices = None
    

    def get_constraint(self):
        self.validate_values()

        services_times_list = [
            random.randint(
                self.min_service_time, 
                self.max_service_time
            ) for i in range(self.number_of_points)
        ]

        services_times = {}
        for i in range(len(services_times_list)):
            services_times[self.points_indices[i]] = services_times_list[i]

        return {"services_times": services_times}


    def get_dynamic_setting_elements(self):
        services_attributes_to_problem = {
            "number_of_points" : "number_of_points",
            "points_indices" : "points_indices"
        }
        return services_attributes_to_problem


    def validate_values(self):
        if (self.number_of_points is None or self.number_of_points <= 0):
            raise exceptions.GreaterThanZeroParameter(
                "ServiceTime.number_of_points"
            )

        if (self.min_service_time is None and self.max_service_time is None):
            raise exceptions.MinOrMaxGreaterThanZero(
                "ServiceTime.min_service_time", 
                "ServiceTime.max_service_time"
            )

        if (self.min_service_time <= 0 and self.max_service_time <= 0):
            raise exceptions.MinOrMaxGreaterThanZero(
                "ServiceTime.min_service_time", 
                "ServiceTime.max_service_time"
            )

        if (self.min_service_time is None):
            self.min_service_time = self.max_service_time
        
        if (self.max_service_time is None):
            self.max_service_time = self.min_service_time

        if (self.min_service_time is not None):
            if (self.max_service_time < self.min_service_time):
                raise exceptions.MaxMustBeGreaterThanMin(
                    "ServiceTime.min_service_time", 
                    "ServiceTime.max_service_time"
                )

            if (self.min_service_time < 0):
                raise exceptions.ValueCannotBeNoneNegative(
                    "ServiceTime.min_service_time"
                )
