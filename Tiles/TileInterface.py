from abc import ABC, abstractmethod, abstractproperty
class TileInterface(ABC):
    @abstractmethod
    def get_char(self):
        return
    
    # responsibility of this class to draw itself in the boundaries given
    @abstractmethod
    def draw_pygame_representation(self, game_screen, minX, maxX, minY, maxY):
        pass