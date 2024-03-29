import numpy
import random

from src.constraints.Constraint import Constraint

from src import exceptions

class HomogeneousCapacity(Constraint):
    def __init__(self):
        super().__init__("Capacity Constraint")
        self.capacity = None


    def get_constraint(self):
        self.validate_values()

        return {"capacity": self.capacity}
    

    def get_dynamic_setting_elements(self):
        return {}


    def validate_values(self):
        if (self.capacity is None or self.capacity == 0):
            raise exceptions.GreaterThanZeroParameter(
                "HomogeneousCapacity.capacity"
            )

