from abc import ABC, abstractmethod

from src import exceptions


class ProblemClass(ABC):
    
    instance = None
    
    ### Obrigatory for all Porblems ###
    
    # Acquired from configuration file
    number_of_points = None
    constraints_objects = None
    output_path = None
    output_name = None
    output_type = "text"
    
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


    def make_matrix_edges(self, edge_title, matrix, points_mapping=None):
        text = ""
        text += edge_title + "\n"

        if (points_mapping is None):
            
            for line in matrix:
                for i in range(len(line)-1):
                    item = int(line[i])
                    text += str(item) + " "
                text += str(int(line[-1]))
                text += "\n"
            
        else:
            for i in range(1, len(points_mapping)+1):
                point_index = points_mapping[i]

                for j in range(1, len(points_mapping)):
                    other_point_index = points_mapping[j]

                    value = int(matrix[point_index][other_point_index])

                    text += str(value) + " "

                other_point_index = points_mapping[len(points_mapping)]

                value = int(matrix[point_index][other_point_index])
                text += str(value) + " "
                text += "\n"


        return text


    def write_file(self):
        if (self.output_type == "text"):
            self.write_text_file()
            return
        if (self.output_type == "json"):
            self.write_json_file()
            return


    @abstractmethod
    def get_constraints_generation_order(self):
        pass


    @abstractmethod
    def get_dynamic_setting_dict(self, constraint_class):
        pass


    @abstractmethod
    def update_problem_class(self, constraint_dict):
        pass


    @abstractmethod
    def write_text_file(self):
        pass
    

    @abstractmethod
    def write_json_file(self):
        pass

