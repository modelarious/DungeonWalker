from models.CharacterModel import CharacterModel
from controllers.mvc.PlayerController import PlayerController
from views.CharacterView import CharacterView

# type hints
from models.MapModel import MapModel
from helpers.Camera import Camera

class PlayerControllerPlayerModelFactory():
	def __init__(self, grid_size: int, mapModel: MapModel, camera: Camera):
		self._grid_size = grid_size
		self.mapModel = mapModel
		self.camera = camera

	def getController(self):
		GREEN = (0, 255, 0)

		start_x, start_y = self.mapModel.get_starting_coordinates()
		playerModel = CharacterModel(start_x, start_y)
		playerCharacterView = CharacterView(self._grid_size, GREEN, self.camera)
		playerController = PlayerController(playerCharacterView, playerModel, self.mapModel)

		return playerController, playerModel

