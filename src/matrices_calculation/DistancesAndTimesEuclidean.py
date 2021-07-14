import numpy
import copy
import sklearn.metrics

from src.matrices_calculation import DistancesAndTimesCalculator

class DistancesAndTimesEuclidean(DistancesAndTimesCalculator):
    def __init__(self):
        super().__init__("Euclidean Distances")

    def calculate_dist_and_time_from_source(self, source_position, points):

        source_array = numpy.array([points[source_position]])

        points_array = numpy.array(points)

        distances = sklearn.metrics.pairwise.euclidean_distances(
            source_array, 
            points_array
        )

        distances = numpy.squeeze(distances)
        distances[source_position] = 0

        distances = distances * 100

        times = copy.deepcopy(distances)


        return (distances, times)



