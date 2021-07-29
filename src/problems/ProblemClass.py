import json

from abc import ABC, abstractmethod

from src import exceptions, subproblems


class ProblemClass(ABC):
    
    instance = None
    
    ### Obrigatory for all Porblems ###
    
    # Acquired from configuration file
    number_of_points = None
    constraints_objects = None
    subproblems = None
    output_path = None
    output_name = None
    output_type = "json"
    
    # Acquired while running
    points = None
    distance_matrix = None
    time_matrix = None



    def __new__(cls, *args, **kwargs):
        for subcls in cls.__subclasses__():
            if (subcls.instance is not None):
                return subcls.instance
        
        if (cls.instance is None):
            cls.instance = super(ProblemClass, cls).__new__(
                cls, *args, **kwargs
            )
        
        return cls.instance

    def __init__(self, problem_class_name):
        self.name = problem_class_name


    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute(
                self.__class__.__name__, 
                name
            )
        
        self.__setattr__(name, value)


    def write_file(self):
        if (self.output_path[-1] != "/"):
            self.output_path += "/"

        output_file_name = self.output_path + self.output_name 
        output_file_name += "_sol." + self.output_type

        if (self.output_type == "json"):
            self.write_json_file(output_file_name)
            return
        
        self.write_generic_file(output_file_name)


    def write_final_data(self, running_data):
        if (self.output_path[-1] != "/"):
            self.output_path += "/"

        json_output_file_name = ""
        json_output_file_name += self.output_path 
        json_output_file_name += "running_data_"
        json_output_file_name += self.output_name 
        json_output_file_name += ".json"
        with open(json_output_file_name, "w") as output_file:
            output_file.write(json.dumps(running_data, indent=2))


    @abstractmethod
    def get_constraints_generation_order(self):
        pass


    @abstractmethod
    def update_problem_class(self, constraint_dict):
        pass


    @abstractmethod
    def write_generic_file(self, output_file_name):
        pass
    

    @abstractmethod
    def write_json_file(self, output_file_name):
        pass

