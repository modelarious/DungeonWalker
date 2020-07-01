from controllers.mvc.CharacterController import CharacterController
from pygame import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, event
from helpers.Direction import Left, Right, Up, Down

playerInputToActionMap = {
	K_LEFT : Left(),
	K_RIGHT : Right(),
	K_UP : Up(),
	K_DOWN : Down()
}

class PlayerController(CharacterController):
	
	# move the player if the input requests it
	# XXX template method pattern could be useful here
	def handleInputEvent(self, event: event):
		# we only care about keys being pressed down
		if event.type != KEYDOWN:
			return False
		
		# retrieve the direction for this input or `None` if we don't use the given input in the game
		direction = playerInputToActionMap.get(event.key)
		if direction == None:
			return False

		# prevent the player from moving to a invalid space
		orig_pos = self._characterModel.get_pos()
		speculative_new_player_pos = self._characterModel.get_speculative_position(direction)
		if not self._mapController.is_legal_move(orig_pos, speculative_new_player_pos):
			return False
		
		# move the player
		self._characterModel.move(direction)
		return True
	
	def player_has_won(self):
		if self._characterModel.get_pos() == self._mapController.get_goal_space_coords():
			return True
		return False
	
	def place_player_at_start(self):
		start_coords = self._mapController.get_starting_coordinates()
		self._characterModel.set_pos(*start_coords)
