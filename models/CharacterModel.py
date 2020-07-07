
from abc import ABC, abstractmethod

# I'm imagining that an ai input device would want to 
# use this interface, so I want to bake it into the design
class MoveSetInterface(ABC):

    # @abstractmethod
    # def attack(self, direction):
    #     pass

    @abstractmethod
    def move(self, direction):
        pass

class CharacterModel(MoveSetInterface):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def move(self, direction):
        self._x, self._y = self.get_speculative_position(direction)
    
    def get_pos(self):
        return (self._x, self._y)
    
    def set_pos(self, x, y):
        self._x, self._y = x, y
    
    def get_speculative_position(self, direction):
        return direction.move(self._x, self._y)
