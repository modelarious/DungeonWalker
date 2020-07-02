from controllers.mvc.ControllerBaseClass import ControllerBaseClass

# type hints
from controllers.mvc.MapController import MapController
from models.CharacterModel import CharacterModel
from views.CharacterView import CharacterView

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
	
	def movement_valid(self, direction):
		# prevent the player from moving to a invalid space
		orig_pos = self._characterModel.get_pos()
		speculative_new_player_pos = self._characterModel.get_speculative_position(direction)

		# XXX this is not how a controller should be used... it should be asking the model
		if not self._mapController.is_legal_move(orig_pos, speculative_new_player_pos):
			return False
		
		# valid move
		return True