from settings import MIN_BOARD_WIDTH, MIN_BOARD_HEIGHT, charSet
from exceptions import PointOutsideBoard, BoardTooSmall
from copy import copy
import numpy as np


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
	
	def update(self, otherMapModel):
		self.width = otherMapModel.width
		self.height = otherMapModel.height
		self._board = otherMapModel._board
		self.starting_point = otherMapModel.starting_point
		self.goal_point = otherMapModel.goal_point
		self.enemySpawnPoints = otherMapModel.enemySpawnPoints

	def _create_empty_board(self):
		board = []
		for y in range(self.height):
			blankRow = [charSet["blocked"]]*self.width
			board.append(blankRow)
		return board
	
	def get_board(self):
		return self._board
	
	def get_part_of_board(self, minX, maxX, minY, maxY):
		board = np.array(self._board)
		return board[minY:maxY,minX:maxX]
	
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

		# reject moves that put the player off the board
		if not self.point_in_board(prospective_pos):
			return False

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
			candidateNeighbors = [(x + offX, y + offY) for offX, offY in offsets]
			neighborsWithinBoard = list(filter(self.point_in_board, candidateNeighbors))
			return neighborsWithinBoard

		return []
	
	def get_all_eight_surrounding_neighbors_and_self(self, point):
		# 3x3 matrix of tiles with `point` at the center
		#neighbors = [
		#	[charSet["blocked"], charSet["blocked"], charSet["blocked"]],
		#	[charSet["blocked"], charSet["blocked"], charSet["blocked"]],
		#	[charSet["blocked"], charSet["blocked"], charSet["blocked"]]
		#]
		neighbors = []
		if self.point_in_board(point):
			x, y = point

			# build a 3x3 array (so maxRowLength = 3)
			row = []
			maxRowLength = 3
			for offset in NeighborOffsets:

				# offset from center tile
				offX, offY = offset.value
				appliedOffset = (x + offX, y + offY)

				# default is blocked tile. This way tiles that are off the board are considered blocked.
				# If the tile is on the board, get the actual tile instead
				if self.point_in_board(appliedOffset):
					tile = self.get_tile(appliedOffset)
				else:
					tile = charSet["blocked"]

				# track this tile
				row.append(tile)

				# if we have filled the row, append it
				if len(row) == maxRowLength:
					neighbors.append(row)
					row = []

		return neighbors
	
	def __iter__(self):
		return MapModelIterator(self)

#generates all points inside the map and returns a point tuple each time it's called
class MapModelIterator:
	def __init__(self, mapModel):
		self._mapModel = mapModel

		# data store for tuples of form (x, y)
		self._points = []

		# index into the data store array
		self._index = 0

		self._populate_points()
	
	def _populate_points(self):
		for x in range(self._mapModel.get_width()):
			for y in range(self._mapModel.get_height()):
				self._points.append((x, y))

	# returns the next point tuple (x, y)
	def __next__(self):
		if self._index >= len(self._points):
			raise StopIteration

		point = self._points[self._index]
		self._index += 1
		return point
