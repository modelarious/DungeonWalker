from controllers.mvc.ControllerBaseClass import ControllerBaseClass
from pygame import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, event
from helpers.Direction import Left, Right, Up, Down

# type hints
from controllers.mvc.MapController import MapController
from models.PlayerCharacterModel import PlayerCharacterModel
from views.PlayerCharacterView import PlayerCharacterView


playerInputToActionMap = {
	K_LEFT : Left(),
	K_RIGHT : Right(),
	K_UP : Up(),
	K_DOWN : Down()
}

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
	
	# move the player if the 
	def handleInputEvent(self, event: event):
		# we only care about keys being pressed down
		if event.type != KEYDOWN:
			return False
		
		# retrieve the direction for this input or `None` if we don't use the given input in the game
		direction = playerInputToActionMap.get(event.key)
		if direction == None:
			return False

		self._player.move(direction)
		return True
		
