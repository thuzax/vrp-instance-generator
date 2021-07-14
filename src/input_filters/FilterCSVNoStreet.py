from src.input_filters import Filter

class FilterCSVNoStreet(Filter):
    def __init__(self):
        super().__init__("Filter removing elements with no street")
        self.street_key_name = None

    def apply_filter(self, data):
        """
        Remove points nased on the address street
        """
        
        # Remove rows without street
        data = data.dropna(subset=[self.street_key_name])

        return data