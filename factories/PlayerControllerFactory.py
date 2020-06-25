from models.PlayerCharacterModel import PlayerCharacterModel
from controllers.mvc.PlayerController import PlayerController
from views.PlayerCharacterView import PlayerCharacterView

# type hints
from controllers.mvc.MapController import MapController

class PlayerControllerFactory():
	def __init__(self, grid_size: int, mapController: MapController):
		self._grid_size = grid_size
		self.mapController = mapController

	def getController(self):
		start_x, start_y = self.mapController.get_starting_coordinates()
		print(f"start coordinates: {start_x}, {start_y}")
		playerModel = PlayerCharacterModel(start_x, start_y)
		playerCharacterView = PlayerCharacterView(self._grid_size)
		playerController = PlayerController(playerCharacterView, playerModel, self.mapController)

		return playerController

