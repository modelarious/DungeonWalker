from abc import ABC, abstractmethod

class MapGeneratorBaseClass(ABC):
    def __init__(self, mapModel):
        self.mapModel = mapModel
    
    @abstractmethod
    def generateMap(self):
        return self.mapModel