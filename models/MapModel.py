from settings import MIN_BOARD_WIDTH, MIN_BOARD_HEIGHT, charSet
from exceptions import PointOutsideBoard, BoardTooSmall
from copy import copy


# XXX you made the data returned by get_* functions a copy of the internal data.. do you need this immutability?
class MapModel():
	def __init__(self, width, height):
		if width < MIN_BOARD_WIDTH or height < MIN_BOARD_HEIGHT: raise BoardTooSmall

		self.width = width
		self.height = height

		self._board = self._create_empty_board()

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
	
	def get_neighbors(self, currPoint):
		if self.point_in_board(currPoint):
			currX, currY = currPoint
			offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
			candidates = [(currX + offX, currY + offY) for offX, offY in offsets]
			candidates = list(filter(self.point_in_board, candidates))
			return candidates

		return []
