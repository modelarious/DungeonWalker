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