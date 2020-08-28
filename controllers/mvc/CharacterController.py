from controllers.mvc.ControllerBaseClass import ControllerBaseClass

# type hints
from models.MapModel import MapModel
from models.CharacterModel import CharacterModel
from views.CharacterView import CharacterView

class CharacterController(ControllerBaseClass):
	def __init__(self, 
			characterView: CharacterView,
			characterModel: CharacterModel,
			mapModel: MapModel):

		self._characterView = characterView
		self._characterModel = characterModel
		self._mapModel = mapModel
	
	def updateView(self, game_screen):
		self._characterView.updateView(game_screen, self._characterModel)

	# XXX this should be abolished!
	def get_pos(self):
		return self._characterModel.get_pos()
	
	# prevent the player from moving to a invalid space
	# XXX also not how a controller should be used. 
	# XXX Move the "movement_valid" and "movement_prevented" functions to
	# XXX a separate class
	def movement_valid(self, direction, characterModel):
		orig_pos = characterModel.get_pos()
		speculative_new_player_pos = characterModel.get_speculative_position(direction)
		return self._mapModel.is_legal_move(orig_pos, speculative_new_player_pos)
	
	def movement_prevented(self, direction, preventedPositions):
		# XXX GROSS, ask the model!!!
		speculative_new_player_pos = self._characterModel.get_speculative_position(direction)
		return speculative_new_player_pos in preventedPositions