from abc import ABC, abstractmethod

import numpy

from src import exceptions

class DistancesAndTimesCalculator(ABC):

    instance = None
    

    # Acquired by subclass
    method = None
    
    # Acquired from config file (using ProblemClass)
    log_file_name = None
    log_file = None

    # Acquired while running
    points = None

    def __new__(cls, *args, **kwargs):
        for subcls in cls.__subclasses__():
            if (subcls.instance is not None):
                cls.instance = subcls.instance
        
        if (cls.instance is None):
            cls.instance = super(DistancesAndTimesCalculator, cls).__new__(
                cls, *args, **kwargs
            )
        return cls.instance


    def __init__(self, method):

        self.method = method.lower()


    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute(
                self.__class__.__name__, 
                name
            )
        
        self.__setattr__(name, value)



    def calculate_distances_and_times(self):
        """Return two NxN matrices representing (respectively) the time and distance matrix.
        """

        distance_matrix = []
        time_matrix = []

        for i in range(len(self.points)):
            results = self.calculate_dist_and_time_from_source(
                                                i, 
                                                self.points
                                            )

            distances, times = results
            if (distances is None or times is None):
                raise exceptions.DistanceToPointCannotBeCalculated(
                    self.points[i]
                )

            distance_matrix.append(distances)
            time_matrix.append(times)

        distance_matrix = numpy.array(distance_matrix)
        distance_matrix = numpy.around(distance_matrix)

        time_matrix = numpy.array(time_matrix)
        time_matrix = numpy.around(time_matrix)
        

        return (distance_matrix, time_matrix)


    def set_log_file(self, output_log_file_path, output_file_name):
        if (output_log_file_path[-1] != "/"):
            output_log_file_path = output_log_file_path + "/"

        self.log_file_path = output_log_file_path + "#"
        self.log_file_path +=  output_file_name + "_mat_calc." + "log"


    @abstractmethod
    def calculate_dist_and_time_from_source(self, source_position, points):
        pass
