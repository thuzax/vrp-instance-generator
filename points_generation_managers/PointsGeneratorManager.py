from abc import ABC, abstractmethod

from src import exceptions

class PointsGeneratorManager(ABC):

    instance = None

    # Acquired by subclass
    file_type = None

    # From configuration file
    input_path = None
    input_name = None
    filters = None

    # While running
    data = None
    selected_items = None

    def __new__(cls, *args, **kwargs):
        for subcls in cls.__subclasses__():
            if (subcls.instance is not None):
                cls.instance = subcls.instance
        
        if (cls.instance is None):
            cls.instance = super(PointsGeneratorManager, cls).__new__(
                cls, *args, **kwargs
            )
        return cls.instance

    def __init__(self, file_type):

        self.file_type = file_type.lower()


    @abstractmethod
    def read_from_file_type(self, instance_name):
        pass

    @abstractmethod
    def select_points(self, number_of_points):
        pass

    @abstractmethod
    def apply_filters(self, data):
        pass

    @abstractmethod
    def remove_invalids(self, data):
        pass

    @abstractmethod
    def write_selected_items_in_file_type(self, output):
        pass


    def read_file(self):
        if (self.input_path[-1] != "/"):
            self.input_path = self.input_path + "/"

        instance_name = self.input_path + self.input_name + "." + self.file_type

        data_frame = self.read_from_file_type(instance_name)

        data_frame = self.remove_invalids(data_frame)
        
        self.data = self.apply_filters(data_frame)


    def write_selected_items(self, output_path, output_name):
        if (output_path[-1] != "/"):
            output_path = output_path + "/"

        output = output_path + output_name + "_selected_items" + ".csv"
        self.write_selected_items_in_file_type(output)


    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute(
                "PointsGeneratorManager", 
                name
            )
        
        self.__setattr__(name, value)

