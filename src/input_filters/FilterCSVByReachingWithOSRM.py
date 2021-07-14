import pandas

from src import matrices_calculation
from src.input_filters import Filter

class FilterCSVByReachingWithOSRM(Filter):
    def __init__(self):
        super().__init__("Filter by Reaching")

        self.first_coordenate_name = None
        self.second_coordenate_name = None

    def apply_filter(self, data):
        removed_set = pandas.DataFrame(columns=data.columns)

        osrm_dist_and_time_calc = matrices_calculation.DistancesAndTimesOSRM()

        for ind, row in data.iterrows():
            random_ind = data.sample(n=1).index
            while(ind == random_ind):
                random_ind = data.sample(n=1).index

            random_row = data.loc[random_ind].iloc[0]

            point_x = (
                float(row[self.first_coordenate_name]), 
                float(row[self.second_coordenate_name])
            )

            point_y = (
                float(random_row[self.first_coordenate_name]), 
                float(random_row[self.second_coordenate_name])
            )

            distance, time = osrm_dist_and_time_calc.request_dist_and_time(
                                                        point_x, 
                                                        point_y
                                                    )

            if ((distance is None) or (time is None)):
                removed_set = removed_set.append(row)


        data = data.drop(removed_set.index)
        return data

