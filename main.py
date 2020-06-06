from factories.GridControllerFactory import GridControllerFactory
from factories.MapControllerFactory import MapControllerFactory
from controllers.GameController import GameController

class Colors():
	def __init__(self):
		self.BLACK = (255, 255, 255)

max_x = 1024
max_y = 768
grid_size = 32
colors = Colors()
gridController = GridControllerFactory(
	max_x=max_x, max_y=max_y, grid_size=grid_size, colors=colors
).getController()

mapController = MapControllerFactory(
	max_x_grid_spaces=max_x//grid_size,
	max_y_grid_spaces = max_y//grid_size
).getController()

gameController = GameController(gridController, mapController)

gameController.main_loop()
