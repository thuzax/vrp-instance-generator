from abc import ABC, abstractmethod

from src import exceptions

class Filter(ABC):

    def __init__(self, filter_name):
        self.filter_name = filter_name

    @abstractmethod
    def apply_filter(self, data):
        pass

    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute("Filter", name)
        self.__setattr__(name, value)

