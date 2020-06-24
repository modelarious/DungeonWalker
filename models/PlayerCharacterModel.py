
from abc import ABC, abstractmethod
from helpers.Direction import Left, Right, Up, Down

# I'm imagining that an ai input device would want to 
# use this interface, so I want to bake it into the design
class MoveSetInterface(ABC):

    # @abstractmethod
    # def attack(self, direction):
    #     pass

    @abstractmethod
    def move(self, direction):
        pass

class Character(MoveSetInterface):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def move(self, direction):
        self._x, self._y = direction.move(self._x, self._y)
    
    def get_pos(self):
        return (self._x, self._y)
    
    def set_pos(self, x, y):
        self._x, self._y = x, y
    

# this level of abstraction may not be needed right now, but I'm pretty sure 
# enemies will inherit from Character as well and will need some differentiation
class PlayerCharacterModel(Character):
    def hello(self):
        pass
