from abc import ABC, abstractmethod

from src import exceptions

class Constraint(ABC):
    def __init__(self, constraint_name):
        self.constraint_name = constraint_name

    @abstractmethod
    def get_constraint(self):
        pass

    @abstractmethod
    def validate_values(self):
        pass

    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute("ProblemClass", name)
        self.__setattr__(name, value)

