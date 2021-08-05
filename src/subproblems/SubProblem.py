from abc import ABC, ABCMeta, abstractmethod

from src import exceptions

class SubProblem(metaclass=ABCMeta):

    instance = None
    output_dict_keys = None
    
    def __new__(cls, *args, **kwargs):
        if (cls.instance is None):
            cls.instance = super(SubProblem, cls).__new__(
                cls, *args, **kwargs
            )
        
        return cls.instance


    def __init__(self, subproblem_name):
        self.subproblem_name = subproblem_name


    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute(
                self.__class__.__name__, 
                name
            )
        self.__setattr__(name, value)


    def solve_subproblem(self):
        self.get_subproblem_instance()
        self.solve_instance()
        self.get_subproblem_result()

        solution_dict = {}
        for item in self.output_dict_keys:
            solution_dict[item] = self.__dict__.get(item)

        return solution_dict


    @abstractmethod
    def get_subproblem_instance(self):
        pass
    
    @abstractmethod
    def solve_instance(self):
        pass

    @abstractmethod
    def get_subproblem_result(self):
        pass
    
    @abstractmethod
    def get_dynamic_setting_elements(self):
        pass