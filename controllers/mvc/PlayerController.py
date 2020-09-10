from controllers.mvc.CharacterController import CharacterController
from pygame import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, event
from helpers.Direction import Left, Right, Up, Down, NullMove

playerInputToActionMap = {
	K_LEFT : Left(),
	K_RIGHT : Right(),
	K_UP : Up(),
	K_DOWN : Down(),
	K_SPACE : NullMove(),
}

class PlayerController(CharacterController):
	
	# move the player if the input requests it
	# return False if the Player didn't move in reaction to the input else return 
	# True if the Player succeeded in moving
	def handleInputEvent(self, event: event):
		# we only care about keys being pressed down
		if event.type != KEYDOWN:
			return False
		
		# retrieve the direction for this input or 
		# `None` if we don't use the given input in the game (example: the 'p' key is unused)
		direction = playerInputToActionMap.get(event.key)
		if direction == None:
			return False
		
		# If this isn't a valid move for the player to make, return false
		if not self._characterModel.movement_valid(direction, self._mapModel):
			return False
		
		# actually perform the movement
		self._characterModel.move(direction)
		return True

	# XXX this is not how a controller should be used... it should be asking the model
	def player_has_won(self):
		return self._characterModel.get_pos() == self._mapModel.get_goal_space_coords()
	
	# XXX this is not how a controller should be used... it should be asking the model
	def place_player_at_start(self):
		start_coords = self._mapModel.get_starting_coordinates()
		# XXX MAP IS NOT BEING UPDATED HERE!!
		self._characterModel.set_pos(*start_coords)
