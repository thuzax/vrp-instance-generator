from src.input_filters import Filter

class FilterCSVNoNumbered(Filter):
    def __init__(self):
        super().__init__("Filter removing elements with no number")
        self.number_key_name = None


    def apply_filter(self, data):
        """
        Remove points nased on the address number
        """
        
        # Remove rows without number
        data = data.dropna(subset=[self.number_key_name])

        return data