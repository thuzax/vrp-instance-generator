import numpy
import random
import math
import scipy.spatial
import sklearn.cluster
import matplotlib.pyplot
from numpy.core.defchararray import center

from src import exceptions
from constraints.Constraint import Constraint

class UrbanRuralAptitude(Constraint):
    def __init__(self):
        super().__init__("Urban and Rural Aptitude Constraint")
        
        self.per_number_urban_centers = None
        self.max_urban_distance = None
        self.method = None

        # must be setted dynamically
        self.points = None

    def generate_aptitude(self, number_urban_centers):

        distances_to_center = None

        if (self.method == "clustering"):
            distances_to_center = (
                self.generate_aptitude_by_clustering(number_urban_centers)
            )

        if (self.method == "center_seeds"):
            distances_to_center = (
                self.generate_aptitude_by_center_seeds(number_urban_centers)
            )

        if (distances_to_center is None):
            return None

        points_classif = (
            self.classify_using_distances_to_center(distances_to_center)
        )

        for i, point in enumerate(self.points):
            if (points_classif[i] == "u"):
                matplotlib.pyplot.scatter(
                    point[0],
                    point[1],
                    color="blue"
                )
            if (points_classif[i] == "r"):
                matplotlib.pyplot.scatter(
                    point[0],
                    point[1],
                    color="red"
                )

        # matplotlib.pyplot.show()
        # output_path = global_parameters.output_path()
        # output_name = global_parameters.output_name()

        # matplotlib.pyplot.gca().set_aspect('equal', adjustable='box')
        # matplotlib.pyplot.xticks(rotation=-15)

        # fig_name = output_path + "/" + "fig_" + output_name + ".png"
        # matplotlib.pyplot.savefig(fig_name)

        return points_classif


    def generate_aptitude_by_clustering(self, number_of_clusters):

        points_arr = numpy.array(self.points)

        kmeans = sklearn.cluster.KMeans(n_clusters=number_of_clusters)
        kmeans.fit(points_arr)
        
        matplotlib.pyplot.scatter(
            kmeans.cluster_centers_[:,0],
            kmeans.cluster_centers_[:,1],
            color="black"
        )
        for x,y in kmeans.cluster_centers_:
            matplotlib.pyplot.annotate(
                "center",
                (x,y),
                textcoords="offset points",
                xytext=(0,10),
                ha="center"
            )

        distances_to_center = scipy.spatial.distance.cdist(
                        points_arr,
                        kmeans.cluster_centers_,
                        metric="euclidean"
                    )

        return distances_to_center


    def generate_aptitude_by_center_seeds(self, number_of_seeds):

        points_set = set(self.points)

        center_seeds = set()

        first_point = self.points[random.randint(0, len(self.points)-1)]

        center_seeds.add(first_point)
        number_of_seeds -= 1

        points_set.remove(first_point)

        candidates_set_size = math.ceil(len(self.points)**(1/2))

        while(number_of_seeds > 0):
            candidates_set = random.sample(points_set, candidates_set_size)

            number_of_seeds -= 1

            candidates_arr = numpy.array(candidates_set)
            center_seeds_arr = numpy.array(list(center_seeds))


            distances = scipy.spatial.distance.cdist(
                                        candidates_arr, 
                                        center_seeds_arr,
                                        metric="euclidean"
                                    )

            seed_position = numpy.argmax(numpy.amin(distances, axis=1))

            center_seeds.add(candidates_set[seed_position])
            points_set.remove(candidates_set[seed_position])

        points_arr = numpy.array(self.points)
        center_seeds_arr = numpy.array(list(center_seeds))


        matplotlib.pyplot.scatter(
            center_seeds_arr[:,0],
            center_seeds_arr[:,1],
            color="black"
        )
        for x,y in center_seeds_arr:
            matplotlib.pyplot.annotate(
                "center",
                (x,y),
                textcoords="offset points",
                xytext=(0,10),
                ha="center"
            )

        distances_to_center_seeds = scipy.spatial.distance.cdist(
                        points_arr,
                        center_seeds_arr,
                        metric="euclidean"
                    )

        return distances_to_center_seeds


    def classify_using_distances_to_center(self, distances_to_center):
        points_min_distance = numpy.amin(distances_to_center, axis=1)

        urb_rur_points = []

        for i in range(len(self.points)):
            if (points_min_distance[i] == 0 
                and self.method == "clustering"):
                urb_rur_points.append("r")
                continue
            
            if (points_min_distance[i] > self.max_urban_distance):
                urb_rur_points.append("r")
                continue

            urb_rur_points.append("u")

        return urb_rur_points


    def get_constraint(self):
        number_urban_centers = math.ceil(
                                    (
                                        len(self.points) * self.per_number_urban_centers
                                    ) 
                                    / 100
                                )

        urban_rural_aptitude = self.generate_aptitude(number_urban_centers)

        return {"urban_rural_aptitude": urban_rural_aptitude}


    def validate_values(self):
        if (
            self.per_number_urban_centers is None 
            or self.per_number_urban_centers <= 0
        ):
            raise exceptions.GreaterThanZeroParameter(
                "UrbanRuralAptitude.number_of_points"
            )

        if (
            self.max_urban_distance is None 
            or self.max_urban_distance <= 0
        ):
            raise exceptions.GreaterThanZeroParameter(
                "UrbanRuralAptitude.max_urban_distance"
            )


        if (self.method is None):
            raise exceptions.ParamMustBeSetted("UrbanRuralAptitude.method")

        if (self.method is None):
            raise exceptions.ParamMustBeSetted("UrbanRuralAptitude.points")

