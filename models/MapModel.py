from settings import MIN_BOARD_WIDTH, MIN_BOARD_HEIGHT, charSet
from exceptions import PointOutsideBoard, BoardTooSmall
from copy import copy


from enum import Enum
class NeighborOffsets(Enum):
	UPPER_LEFT_CORNER = (-1, -1)
	UPPER_MIDDLE = (0, -1) 
	UPPER_RIGHT_CORNER = (1, -1)
	CENTER_LEFT = (-1, 0)
	CENTER_MIDDLE = (0, 0) 
	CENTER_RIGHT = (1, 0)
	BOTTOM_LEFT_CORNER = (-1, 1)
	BOTTOM_MIDDLE = (0, 1)
	BOTTOM_RIGHT_CORNER = (1, 1)

# XXX you made the data returned by get_* functions a copy of the internal data.. do you need this immutability?
class MapModel():
	def __init__(self, width, height):
		if width < MIN_BOARD_WIDTH or height < MIN_BOARD_HEIGHT: raise BoardTooSmall

		self.width = width
		self.height = height

		self._board = self._create_empty_board()

		# arbitrary defaults that get overwritten
		self.starting_point = (20, 20)
		self.goal_point = (0, 0)

		self.enemySpawnPoints = []
	
	def _create_empty_board(self):
		board = []
		for y in range(self.height):
			blankRow = [charSet["blocked"]]*self.width
			board.append(blankRow)
		return board
	
	def get_board(self):
		return self._board
	
	def get_spawn_points(self):
		return self.enemySpawnPoints

	def add_enemy_spawn_points(self, enemySpawnPoints):
		self.enemySpawnPoints.extend(enemySpawnPoints)
	
	def get_tile(self, point):
		pX, pY = point
		if not self.point_in_board(point):
			raise PointOutsideBoard(
				f"get_tile: board width and height ({self.width}, {self.height}), given point: ({pX, pY})")
		return self._board[pY][pX]

	def change_tile(self, point, char):
		pX, pY = point
		if not self.point_in_board(point):
			raise PointOutsideBoard(
				f"change_tile: board width and height ({self.width}, {self.height}), given point: ({pX, pY})")
		self._board[pY][pX] = char

	def point_in_board(self, pt):
		(pX, pY) = pt
		if pX < 0 or pY < 0:
			return False
		try:
			self._board[pY][pX]
			return True
		except IndexError:
			return False
	
	# print the board to the screen (used to quickly verify the view)
	# XXX can be removed if you don't want to see the board output on the terminal
	def draw_board(self):
		for row in self._board:
			row = list(map(lambda a : a.get_char(), row))
			print("".join(row).replace(charSet["pathTemp"].get_char(), charSet["passable"].get_char())
				.replace(charSet["anchor"].get_char(), charSet["passable"].get_char()))
		print()
	
	def get_width(self):
		return copy(self.width)
	
	def get_height(self):
		return copy(self.height)
	
	def set_starting_tile(self, pt):
		self.change_tile(pt, charSet["start"])
		self.starting_point = pt

	def set_goal_tile(self, pt):
		self.change_tile(pt, charSet["goal"])
		self.goal_point = pt
	
	def get_starting_coordinates(self):
		return self.starting_point

	def get_goal_space_coords(self):
		return self.goal_point
	
	def is_legal_move(self, start_pos, prospective_pos):
		s_x, s_y = start_pos
		p_x, p_y = prospective_pos

		# if the prospective move is more than one space away from current position, reject
		if abs(s_x - p_x) > 1 or abs(s_y - p_y) > 1:
			return False
		
		# prevent character from moving onto a blocked tile
		if self.get_tile(prospective_pos) == charSet["blocked"]:
			return False
		
		return True
	
	def get_neighbors_within_board(self, point):
		if self.point_in_board(point):
			x, y = point
			offsets = (NeighborOffsets.CENTER_LEFT, NeighborOffsets.CENTER_RIGHT, NeighborOffsets.UPPER_MIDDLE, NeighborOffsets.BOTTOM_MIDDLE)
			offsets = [o.value for o in offsets]
			candidates = [(x + offX, y + offY) for offX, offY in offsets]
			candidates = list(filter(self.point_in_board, candidates))
			return candidates

		return []
	
	def get_all_eight_surrounding_neighbors_and_self(self, point):
	#   output = {
	# 	    NeighborOffset.UPPER_LEFT_CORNER : charSet["blocked"],
	#       NeighborOffset.UPPER_RIGHT_CORNER : charSet["blocked"]
	#   }
		neighbors = []
		if self.point_in_board(point):
			x, y = point
			# offsets = (UPPER_LEFT_CORNER, UPPER_MIDDLE, UPPER_RIGHT_CORNER) # this should be using the TilePositions, and those should be made into individual classes
			#candidates = [offset.applyOffset(x, y) for offset in NeighborOffsets]

			# build a 3x3 array (so maxRowLength = 3)
			row = []
			maxRowLength = 3
			for offset in NeighborOffsets:
				offX, offY = offset.value
				appliedOffset = (x + offX, y + offY)

				# default is blocked, unless the space is on the board
				tile = charSet["blocked"] # XXX anywhere you use charSet["blocked"] to indicate that a space should not be useable (or check for charSet[blocked]), you should instead call a function that determines if the space is blocked or not (that way you can add other types of blocked spaces in the future if you want to)

				# if the point is on the board, update the tile value from default (blocked)
				if self.point_in_board(appliedOffset):
					tile = self.get_tile(appliedOffset)
				
				# track this tile
				row.append(tile)

				# if we have filled the row, append it
				if len(row) == maxRowLength:
					neighbors.append(row)
					row = []

		return neighbors
	
	def __iter__(self):
		return MapModelIterator(self)




#generates all points inside the map and returns a tuple each time it's called:
#(point, tile) -> ((x, y), tile)
# XXX clean this up, it currently does (x, y) until we prove it needs to do otherwise
# XXX so rename some functions
class MapModelIterator:
	def __init__(self, mapModel):
		self._mapModel = mapModel

		# data store for tuples of form (x, y)
		self._points = []

		# data store for tuples of form ((x, y), tile)
		# self._pointTilePairs = []

		# index into the data store array
		self._index = 0

		self._populate_point_tile_pairs()
	
	def _populate_point_tile_pairs(self):
		for x in range(self._mapModel.get_width()):
			for y in range(self._mapModel.get_height()):
				# point = (x, y)
				# tile = self._mapModel.get_tile(point)
				# self._pointTilePairs.append( (point, tile) )
				self._points.append((x, y))

	# returns the next (point, tile) tuple
	def __next__(self):
		# if self._index >= len(self._pointTilePairs):
		# 	raise StopIteration
		if self._index >= len(self._points):
			raise StopIteration

		# pointTilePair = self._pointTilePairs[self._index]
		# self._index += 1
		# return pointTilePair

		point = self._points[self._index]
		self._index += 1
		return point
