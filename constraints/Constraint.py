from abc import ABC, abstractmethod

class Constraint(ABC):
    def __init__(self, constraint_name):
        self.constraint_name = constraint_name

    @abstractmethod
    def get_constraint(self):
        pass

    @abstractmethod
    def set_attribute(self, name, value):
        pass