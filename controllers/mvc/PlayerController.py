from controllers.mvc.ControllerBaseClass import ControllerBaseClass
from pygame import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, event
from helpers.Direction import Left, Right, Up, Down

# type hints
from controllers.mvc.MapController import MapController
from models.CharacterModel import CharacterModel
from views.CharacterView import CharacterView


playerInputToActionMap = {
	K_LEFT : Left(),
	K_RIGHT : Right(),
	K_UP : Up(),
	K_DOWN : Down()
}

class CharacterController(ControllerBaseClass):
	def __init__(self, 
			characterView: CharacterView,
			characterModel: CharacterModel,
			mapController: MapController ):

		self._characterView = characterView
		self._characterModel = characterModel
		self._mapController = mapController
	
	def updateView(self, game_screen):
		self._characterView.updateView(game_screen, self._characterModel)


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




# XXX might be better not to give the enemy controller the player controller but instead an object that
# wraps the player model and lets the enemy make queries about the player 
class EnemyController(CharacterController):
	def __init__(self, 
			characterView: CharacterView,
			characterModel: CharacterModel,
			mapController: MapController,
			playerController: PlayerController ):
		super().__init__(characterView, characterModel, mapController)
		self.playerController = playerController

	def update_position(self):
		direction = Right()
		self._characterModel.move(direction)