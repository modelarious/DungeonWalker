
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
		self._previousPositionStack = []

	def move(self, direction):
		self._previousPositionStack.append(self.get_pos())
		self.set_pos(*self.get_speculative_position(direction))
	
	def get_pos(self):
		return (self._x, self._y)
	
	def set_pos(self, x, y):
		self._x, self._y = x, y
	
	def get_speculative_position(self, direction):
		return direction.move(self._x, self._y)

	def undo_move(self):
		self.set_pos(*self._previousPositionStack.pop())
	
	def get_copy(self):
		cp = CharacterModel(*self.get_pos())
		cp._previousPositionStack = self._previousPositionStack[:]
		return cp
	
	# make sure the move is a valid move on the board (not moving into a wall, etc)
	def movement_valid(self, direction, mapModel):
		orig_pos = self.get_pos()
		speculative_new_player_pos = self.get_speculative_position(direction)
		return mapModel.is_legal_move(orig_pos, speculative_new_player_pos)
	
	# check if the character cannot move to the given space
	def movement_prevented(self, direction, preventedPositions):
		speculative_new_player_pos = self.get_speculative_position(direction)
		return speculative_new_player_pos in preventedPositions