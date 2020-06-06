from models.GridModel import GridModel
from views.GridView import GridView
from controllers.GridController import GridController

class GridControllerFactory():
	def __init__(self, max_x, max_y, grid_size, colors):
		self.max_x = max_x
		self.max_y = max_y
		self.grid_size = grid_size
		self.colors = colors
	
	def getController(self):
		bm = GridModel(self.max_x, self.max_y, self.grid_size)
		bv = GridView(self.colors)
		return GridController(bm, bv)

