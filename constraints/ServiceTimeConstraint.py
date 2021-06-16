from src import exceptions
from constraints.Constraint import Constraint
import numpy
import random

class ServiceTimeConstraint(Constraint):
    def __init__(self):
        super().__init__("Service Time Constraint")
        self.max_service_time = None
        self.min_service_time = None
        self.number_of_points = None
    
    def get_constraint(self):
        self.validate_min_max_values()

        services_times = numpy.array([
                        random.randint(
                            self.min_service_time, 
                            self.max_service_time
                        ) for i in range(self.number_of_points)
                    ])
        
        return services_times

    def validate_min_max_values(self):
        if (self.number_of_points is None or self.number_of_points == 0):
            raise exceptions.GreaterThanZeroParameter("number_of_points")

        if (self.min_service_time is None and self.max_service_time is None):
            raise exceptions.GreaterThanZeroMinAndMaxServicesTimes()

        if (self.min_service_time is not None):
            if (self.max_service_time < self.min_service_time):
                raise exceptions.MinServiceTimeGreaterThanMax()

            if (self.min_service_time < 0):
                raise exceptions.MinServiceTimeCannotBeNoneNegative()

        else:
            self.min_service_time = self.max_service_time
        
        if (self.max_service_time is None):
            self.max_service_time = self.min_service_time

    def set_attribute(self, name, value):
        self.__setattr__(name, value)