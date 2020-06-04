import pygame, sys
from pygame.locals import *
from abc import ABC, abstractmethod
from itertools import repeat



# defines an interface that all views must provide
class ViewBaseClass(ABC):
	@abstractmethod
	def updateView(self, game_screen, model_response):
		pass
		
class ControllerBaseClass(ABC):
	@abstractmethod
	def updateView(self, game_screen):
		pass

# contract to ensure this interface is enforced between the view and the model
class BoardModel(object):
	def __init__(self, max_x, max_y, grid_size):
		self.max_x = max_x
		self.max_y = max_y
		self.game_dimensions = (max_x, max_y)
		self.grid_size = grid_size
	
	def _y_grid_iter(self):
		return range(self.max_y, 0, -self.grid_size)
	
	def _x_grid_iter(self):
		return range(self.max_x, 0, -self.grid_size)
		
# this works but I thought it would make for a more confusing solution
# 	def _iter(self, x=None, y=None):
# 		if x == None:
# 			x = self._x_grid_iter()
# 		else:
# 			x = repeat(x)
# 			
# 		if y == None:
# 			y = self._y_grid_iter()
# 		else:
# 			y = repeat(y)
# 		
# 		# will be two iterators
# 		return zip(x, y)
		
	def _max_x_iter(self):
		return zip(repeat(self.max_x), self._y_grid_iter())
	
	def _min_x_iter(self):
		return zip(repeat(0), self._y_grid_iter())
	
	def _max_y_iter(self):
		return zip(self._x_grid_iter(), repeat(self.max_y))
	
	def _min_y_iter(self):
		return zip(self._x_grid_iter(), repeat(0))
	
	# returns a list like [ ((1024, 32), (0, 32)), ((1024, 64), (0, 64)) ... ]
	# each tuple contains two points: the starting and ending point for a horizontal
	# line.  Iterating through this object will product a series of horizontal lines
	# spread out evenly based on grid_size
	def horizontal_range(self):
# 		return zip(self._iter(x=self.max_x), self._iter(x=0))
		return zip(self._max_x_iter(), self._min_x_iter())
	
	# returns a list like [ ((32, 768), (32, 0)), ((64, 768), (64, 0)) ... ]
	# each tuple contains two points: the starting and ending point for a vertical
	# line.  Iterating through this object will product a series of vertical lines
	# spread out evenly based on grid_size
	def vertical_range(self):
# 		return zip(self._iter(y=self.max_y), self._iter(y=0))
		return zip(self._max_y_iter(), self._min_y_iter())
		
# draws the grid to the screen using the 
class BoardView(ViewBaseClass):

	def __init__(self, colors):
		self.colors = colors
		
	def updateView(self, game_screen, game_dimensions: BoardModel):
		for start_point, end_point in game_dimensions.horizontal_range():
			pygame.draw.line(game_screen, self.colors.BLACK, start_point, end_point)
		for start_point, end_point in game_dimensions.vertical_range():
			pygame.draw.line(game_screen, self.colors.BLACK, start_point, end_point)


class BoardController(ControllerBaseClass):
	def __init__(self, boardModel, boardView):
		self.boardModel = boardModel
		self.boardView = boardView
	
	def updateView(self, game_screen):
		self.boardView.updateView(game_screen, self.boardModel)
	
	def getGameDimensions(self):
		return self.boardModel.game_dimensions

# all other views are going to accept the pygame instance.
# this controller controls all the other controllers (which have their own little MVC loop).
# when a controller says it has updated it's model, it is queued up to have .updateView(game_screen, model_response) called on it.
# the queue needs to be ordered properly so we draw things in the right order.
# 
# this controller will pass the pygame instance and model response into them
class GameController(object):
	
	def __init__(self, boardController):
		pygame.init()
		self.boardController = boardController
		self.game_screen = pygame.display.set_mode(boardController.getGameDimensions())
		self.main_loop()
	
	def main_loop(self):
		
		
		# run the game loop
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				# draw the grid
				self.boardController.updateView(self.game_screen)
		
				# draw the window onto the screen
				pygame.display.update()

class Colors():
	def __init__(self):
		self.BLACK = (255, 255, 255)

max_x = 1024
max_y = 768
grid_size = 32
bm = BoardModel(max_x, max_y, grid_size)

c = Colors()
bv = BoardView(c)

bc = BoardController(bm, bv)
gc = GameController(bc)




	
		