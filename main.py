from factories.GridControllerFactory import GridControllerFactory
from controllers.GameController import GameController

class Colors():
	def __init__(self):
		self.BLACK = (255, 255, 255)

max_x = 1024
max_y = 768
grid_size = 32
colors = Colors()
bc = GridControllerFactory(max_x, max_y, grid_size, colors).getGridController()

gc = GameController(bc)

gc.main_loop()

