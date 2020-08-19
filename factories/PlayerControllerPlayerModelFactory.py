from models.CharacterModel import CharacterModel
from controllers.mvc.PlayerController import PlayerController
from views.CharacterView import CharacterView

# type hints
from models.MapModel import MapModel

class PlayerControllerPlayerModelFactory():
	def __init__(self, grid_size: int, mapModel: MapModel):
		self._grid_size = grid_size
		self.mapModel = mapModel

	def getController(self):
		GREEN = (0, 255, 0)

		start_x, start_y = self.mapModel.get_starting_coordinates()
		playerModel = CharacterModel(start_x, start_y)
		playerCharacterView = CharacterView(self._grid_size, GREEN)
		playerController = PlayerController(playerCharacterView, playerModel, self.mapModel)

		return playerController, playerModel

