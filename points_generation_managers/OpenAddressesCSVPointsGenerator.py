import pandas

from points_generation_managers import PointsGeneratorManager


class OpenAddressesCSVPointsGenerator(PointsGeneratorManager):

    # From configuration file
    first_coordenate_name = None
    second_coordenate_name = None
    allow_repetition = False

    def __init__(self):
        super().__init__("csv")

    def get_points_coordinates(self, data_sample):
        """Get the latitude and longitude of all rows
        """

        points_list = []

        for ind, row in data_sample.iterrows():
            latitude = row[self.first_coordenate_name]
            longitude = row[self.second_coordenate_name]

            point = (
                float(latitude), 
                float(longitude)
            )

            points_list.append(point)
        
        return points_list


    def select_points(self, number_of_points):

        if (len(self.data) < number_of_points):
            self.selected_items = self.data
        else:
            self.selected_items = self.data.sample(n=number_of_points)

        return self.get_points_coordinates(data_sample=self.selected_items)


    def apply_filters(self, data):
        for item in self.filters:
            data = item.apply_filter(data)
        return data
        


    def remove_invalids(self, data):
         # Remove rows with latidude or longitude with None values
        data = data.dropna(
            subset=[
                self.first_coordenate_name, 
                self.second_coordenate_name
            ]
        )
        
        # Remove rows with invalid latitude
        data = data.drop(
            data[
                (data[self.first_coordenate_name] < -90) 
                | 
                (data[self.first_coordenate_name] > 90)
            ].index
        )

        # Remove rows with invalid longitude
        data = data.drop(
            data[
                (data[self.second_coordenate_name] < -180) 
                | 
                (data[self.second_coordenate_name] > 180)
            ].index
        )

        # Remove reapeated points if --block-point-repetition flag was specified
        if (not self.allow_repetition):
            data = data.drop_duplicates(
                subset=[
                    self.first_coordenate_name, 
                    self.second_coordenate_name
                ], 
                keep="first"
            )
        
        return data


    def read_from_file_type(self, instance_name):
        data_frame = pandas.read_csv(instance_name)
        return data_frame


    def write_selected_items_in_file_type(self, output):
        """Write the data in a CSV file
        """
        self.selected_items.to_csv(output, index=False)
