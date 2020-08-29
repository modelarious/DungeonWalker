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