from controllers.mvc.ControllerBaseClass import ControllerBaseClass

# type hints
from controllers.mvc.MapController import MapController
from models.PlayerCharacterModel import PlayerCharacterModel
from views.PlayerCharacterView import PlayerCharacterView


class PlayerController(ControllerBaseClass):
	def __init__(self, 
			playerCharacterView: PlayerCharacterView, 
			playerModel: PlayerCharacterModel, 
			mapController: MapController ):
			
		self._playerCharacterView = playerCharacterView
		self._player = playerModel
		self._mapController = mapController
	
	def updateView(self, game_screen):
		self._playerCharacterView.updateView(game_screen, self._player)


	# def applyMove(self):
	# 	board = self.mapController.get_map()
	# 	self.player.get_pos()
