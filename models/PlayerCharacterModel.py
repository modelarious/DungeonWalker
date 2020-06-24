
from abc import ABC, abstractmethod
from helpers.Direction import Left, Right, Up, Down

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
    
    # def get_x(self):
    #     return self._x
    
    # def get_y(self):
    #     return self._y
    
    # def change_x(self, x):
    #     self._x = x
    
    # def change_y(self, y):
    #     self._y = y
    
    def get_pos(self):
        return (self._x, self._y)
    
    def set_pos(self, x, y):
        self._x, self._y = x, y
    


# next step is to get the player character moving
# XXX FIRST GET IT SHOWING YOU NIT
class PlayerCharacterModel(Character):
    def hello(self):
        pass
