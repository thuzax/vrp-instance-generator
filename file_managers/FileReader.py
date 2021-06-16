from abc import ABC, abstractmethod

class FileReader(ABC):

    def __init__(self, file_type):
        self.file_type = file_type

    
