import numpy
import random

from src import exceptions
from constraints.Constraint import Constraint

class ServiceTime(Constraint):
    def __init__(self):
        super().__init__("Service Time Constraint")
        self.max_service_time = None
        self.min_service_time = None

        # Must be setted dynamically
        self.number_of_points = None
    

    def get_constraint(self):
        self.validate_values()

        services_times = numpy.array([
            random.randint(
                self.min_service_time, 
                self.max_service_time
            ) for i in range(self.number_of_points)
        ])

        return {"services_times": services_times}


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
