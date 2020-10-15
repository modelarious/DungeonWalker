from models.GridModel import GridModel
from views.GridView import GridView
from controllers.mvc.GridController import GridController
from factories.FactoryBaseClass import FactoryBaseClass


class GridControllerFactory(FactoryBaseClass):
	def __init__(self, max_x, max_y, grid_size):
		self.max_x = max_x
		self.max_y = max_y
		self.grid_size = grid_size

	def getController(self):
		bm = GridModel(
			self.get_copy(self.max_x), 
			self.get_copy(self.max_y), 
			self.get_copy(self.grid_size)
		)
		bv = GridView()
		return GridController(bm, bv)

