from models.PlayerCharacterModel import PlayerCharacterModel
from controllers.mvc.PlayerController import PlayerController
from views.CharacterView import CharacterView

# type hints
from controllers.mvc.MapController import MapController

class PlayerControllerFactory():
	def __init__(self, grid_size: int, mapController: MapController):
		self._grid_size = grid_size
		self.mapController = mapController

	def getController(self):
		GREEN = (0, 255, 0)

		start_x, start_y = self.mapController.get_starting_coordinates()
		playerModel = PlayerCharacterModel(start_x, start_y)
		playerCharacterView = CharacterView(self._grid_size, GREEN)
		playerController = PlayerController(playerCharacterView, playerModel, self.mapController)

		return playerController

