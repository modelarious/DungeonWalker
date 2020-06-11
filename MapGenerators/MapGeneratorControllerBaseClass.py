from abc import ABC, abstractmethod

class MapGeneratorControllerBaseClass(ABC):
    def __init__(self, mapGenerator):
        self.mapGenerator = mapGenerator
    
    @abstractmethod
    def generateMap(self):
        return self.mapGenerator.XXX_SPIT_OUT_BOARD()