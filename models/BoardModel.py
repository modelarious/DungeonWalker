from itertools import repeat

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
		
# this works but I thought it would make for a more confusing solution for myself later
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
	def horizontal_lines(self):
# 		return zip(self._iter(x=self.max_x), self._iter(x=0))
		return zip(self._max_x_iter(), self._min_x_iter())
	
	# returns a list like [ ((32, 768), (32, 0)), ((64, 768), (64, 0)) ... ]
	# each tuple contains two points: the starting and ending point for a vertical
	# line.  Iterating through this object will product a series of vertical lines
	# spread out evenly based on grid_size
	def vertical_lines(self):
# 		return zip(self._iter(y=self.max_y), self._iter(y=0))
		return zip(self._max_y_iter(), self._min_y_iter())
