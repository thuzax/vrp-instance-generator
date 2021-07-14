from abc import ABC, abstractmethod

from src import exceptions

class SubProblem(ABC):

    def __init__(self, subproblem_name):
        self.subproblem_name = subproblem_name
        self.output_dict_keys = None

    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute(
                self.__class__.__name__, 
                name
            )
        self.__setattr__(name, value)

    @abstractmethod
    def get_subproblem_instance(self):
        pass
    
    @abstractmethod
    def solve_instance(self):
        pass

    @abstractmethod
    def get_subproblem_result(self):
        pass
    
    def solve_subproblem(self):
        self.get_subproblem_instance()
        self.solve_instance()
        self.get_subproblem_result()

        solution_dict = {}
        for item in self.output_dict_keys:
            solution_dict[item] = self.__dict__.get(item)

        return solution_dict
    