from abc import ABC, abstractmethod

class MapGenerationDriverBaseClass(ABC):
    def __init__(self, width, height, mapGeneratorEngine):
        self.width = width
        self.height = height
        self.mapGeneratorEngine = mapGeneratorEngine
    
    @abstractmethod
    def generateMap(self):
        return self.mapGeneratorEngine.get_finalized_board()