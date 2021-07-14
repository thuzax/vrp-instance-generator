import numpy
import random
import math
import collections
import scipy.spatial
import sklearn.cluster
import sklearn.metrics
import matplotlib.pyplot
from numpy.core.defchararray import center
from sklearn.utils.extmath import density

from src import exceptions
from constraints.Constraint import Constraint

class UrbanRuralAptitude(Constraint):
    def __init__(self):
        super().__init__("Urban and Rural Aptitude Constraint")
        
        self.per_number_urban_centers = None
        self.max_urban_distance = None
        self.method = None
        self.save_figure = False
        self.show_figure = False
        self.figure_path = None
        self.figure_name = None

        # must be setted dynamically
        self.points = None

        # DBSCAN optional parameters and default values
        self.density_clustering_per_distance = 0.1
        self.density_per_min = 0.05


        self.center_distances_methods = [
            "clustering", 
            "center_seeds", 
            "one_clustering"
        ]

        self.density_methods = [
            "dbscan",
            "optics"
        ]



    def generate_aptitude(self, number_urban_centers):

        distances_to_center = None
        labels = None

        if (self.method == "clustering"):
            distances_to_center = (
                self.generate_aptitude_by_clustering(number_urban_centers)
            )

        if (self.method == "center_seeds"):
            distances_to_center = (
                self.generate_aptitude_by_center_seeds(number_urban_centers)
            )
        
        if (self.method == "one_clustering"):
            distances_to_center = (
                self.generate_aptitude_by_one_clustering()
            )

        if (self.method == "dbscan"):
            labels = (
                self.generate_aptitude_by_DBSCAN_clustering()
            )
        
        if (self.method == "optics"):
            labels = (
                self.generate_aptitude_by_OPTICS_clustering()
            )
        

        # Min number 
        if (
            self.method in self.center_distances_methods
            and distances_to_center is None
        ):
            return None

        if (self.method in self.center_distances_methods):
            points_classif = (
                self.classify_using_distances_to_center(distances_to_center)
            )

        if (self.method in self.density_methods):
            points_classif = (
                self.classify_using_density(self.points, labels)
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

        if (self.show_figure):
            matplotlib.pyplot.show()
        
        if (self.save_figure):

            matplotlib.pyplot.gca().set_aspect('equal', adjustable='box')
            matplotlib.pyplot.xticks(rotation=-15)

            if (self.figure_path[-1] != "/"):
                self.figure_path = self.figure_path + "/"

            fig_name = self.figure_path + "fig_" + self.figure_name + ".png"
            matplotlib.pyplot.savefig(fig_name)

        return points_classif


    def generate_aptitude_by_DBSCAN_clustering(self):
        points_arr = numpy.array(self.points)

        max_lat_lon = numpy.max(points_arr, axis=0)
        max_lat = max_lat_lon[0]
        max_lon = max_lat_lon[1]

        min_lat_lon = numpy.min(points_arr, axis=0)
        min_lat = min_lat_lon[0]
        min_lon = min_lat_lon[1]


        axis_x_size = abs(max_lat - min_lat)
        axis_y_size = abs(max_lon - min_lon)

        min_axis = min(axis_x_size, axis_y_size)
        min_distance_dbscan = abs(
            min_axis 
            * self.density_clustering_per_distance
        )

        if (min_distance_dbscan <= 0):
            min_distance_dbscan = 0.01

        dbscan = sklearn.cluster.DBSCAN(
            eps=min_distance_dbscan,
            metric="haversine",
            min_samples=2
        )

        dbscan.fit(points_arr)

        labels = []
        for i in range(len(dbscan.labels_)):
            if (dbscan.labels_[i] == -1):
                labels.append("unlabeld")
            else:
                labels.append(int(dbscan.labels_[i]))

        return labels

    def generate_aptitude_by_OPTICS_clustering(self):
        points_arr = numpy.array(self.points)

        max_lat_lon = numpy.max(points_arr, axis=0)
        max_lat = max_lat_lon[0]
        max_lon = max_lat_lon[1]

        min_lat_lon = numpy.min(points_arr, axis=0)
        min_lat = min_lat_lon[0]
        min_lon = min_lat_lon[1]


        axis_x_size = abs(max_lat - min_lat)
        axis_y_size = abs(max_lon - min_lon)

        min_axis = min(axis_x_size, axis_y_size)
        min_distance_optics = min_axis * self.density_clustering_per_distance

        optics = sklearn.cluster.OPTICS(
            eps=min_distance_optics,
            metric="haversine",
            cluster_method="dbscan",
            min_samples=2
        )

        optics.fit(points_arr)

        labels = []
        for i in range(len(optics.labels_)):
            if (optics.labels_[i] == -1):
                labels.append("unlabeld")
            else:
                labels.append(int(optics.labels_[i]))

        return labels


    def generate_aptitude_by_one_clustering(self):
        points_arr = numpy.array(self.points)

        kmeans = sklearn.cluster.KMeans(n_clusters=1)
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


    def classify_using_density(self, points, labels):
        dict_label_num_points = dict(collections.Counter(labels))

        densities = {}
        for key, value in dict_label_num_points.items():
            densities[key] = float(value) / float(len(labels))

        urb_rur_points = []

        for index in range(len(points)):
            label = labels[index]
            if (
                label == "unlabeld"
                or densities[label] < self.density_per_min
            ):
                urb_rur_points.append("r")
            else:
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

