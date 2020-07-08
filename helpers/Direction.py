from abc import ABC, abstractmethod
class Direction(ABC):
    @abstractmethod
    def move(self, x, y):
        return (x, y)

class Left(Direction):
    def move(self, x, y):
        return (x - 1, y)

class Right(Direction):
    def move(self, x, y):
        return (x + 1, y)
    
class Up(Direction):
    def move(self, x, y):
        return (x, y - 1)

class Down(Direction):
    def move(self, x, y):
        return (x, y + 1)
    
class NullMove(Direction):
    def move(self, x, y):
        return (x, y)