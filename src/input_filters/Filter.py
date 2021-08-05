from abc import ABC, ABCMeta, abstractmethod

from src import exceptions

class Filter(metaclass=ABCMeta):

    def __init__(self, filter_name):
        self.filter_name = filter_name


    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute(
                self.__class__.__name__, 
                name
            )
        
        self.__setattr__(name, value)


    @abstractmethod
    def apply_filter(self, data):
        pass
