from models.BoardModel import BoardModel
from views.BoardView import BoardView
from controllers.BoardController import BoardController

class BoardControllerFactory():
	def __init__(self, max_x, max_y, grid_size, colors):
		self.max_x = max_x
		self.max_y = max_y
		self.grid_size = grid_size
		self.colors = colors
	
	def getBoardController(self):
		bm = BoardModel(self.max_x, self.max_y, self.grid_size)
		bv = BoardView(self.colors)
		return BoardController(bm, bv)

