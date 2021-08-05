from abc import ABC, ABCMeta, abstractmethod

from src import exceptions

class Constraint(metaclass=ABCMeta):
    def __init__(self, constraint_name):
        self.constraint_name = constraint_name


    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute(
                self.__class__.__name__, 
                name
            )
        self.__setattr__(name, value)


    @abstractmethod
    def get_constraint(self):
        pass

    @abstractmethod
    def get_dynamic_setting_elements(self):
        pass

    @abstractmethod
    def validate_values(self):
        pass

