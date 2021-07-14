from src.input_filters import Filter

class FilterCSVBy2DCoordenates(Filter):
    def __init__(self):
        super().__init__("Filter based on 2D coordenate")
        self.min_first_coordinate = None
        self.max_first_coordinate = None
        self.min_second_coordinate = None
        self.max_second_coordinate = None
        self.first_coordenate_name = None
        self.second_coordenate_name = None

    def filter_first_coord_limits(self, data):
        """Remove points out of the latitude limits, if limits are given
        """

        if (
            (self.min_first_coordinate is None) 
            and (self.max_first_coordinate is None)
        ):
            return data

        if (self.max_first_coordinate is None):
            data = data.drop(
                data[
                    data[self.first_coordenate_name]
                     < self.min_first_coordinate
                ].index
            )

            return data

        if (self.min_first_coordinate is None):
            data = data.drop(
                data[
                    data[self.first_coordenate_name] 
                    > self.max_first_coordinate
                ].index
            )

            return data

        data = data.drop(
            data[
                (data[self.first_coordenate_name] < self.min_first_coordinate) 
                | (data[self.first_coordenate_name] > self.max_first_coordinate)
            ].index
        )

        return data


    def filter_second_coord_limits(self, data):
        """Remove points out of the longitude limits, if limits are given
        """
        
        if (
            (self.min_second_coordinate is None) 
            and (self.max_second_coordinate is None)
        ):
            return data

        if (self.max_second_coordinate is None):
            data = data.drop(
                data[
                    data[self.second_coordenate_name] 
                    < self.min_second_coordinate
                ].index
            )

            return data

        if (self.min_second_coordinate is None):
            data = data.drop(
                data[
                    data[self.second_coordenate_name] 
                    > self.max_second_coordinate
                ].index
            )

            return data

        data = data.drop(
            data[
                (data[self.second_coordenate_name] < self.min_second_coordinate) 
                | (
                    data[self.second_coordenate_name] 
                    > self.max_second_coordinate
                )
            ].index
        )

        return data


    def apply_filter(self, data):
        data = self.filter_first_coord_limits(data)
        data = self.filter_second_coord_limits(data)

        return data
