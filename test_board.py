import unittest

from generateMap import Board
from room import Room
from exceptions import *
from settings import *
from parameterized import parameterized
import copy

minBoardSize = MIN_BOARD_HEIGHT
modestBoardSize = minBoardSize * 4

generalTestBoardParams = (modestBoardSize, modestBoardSize - 3)

# used to test if points are reported as inside or outside the board
# will be an array of entries of form
# [ String:name, 2-entry-tuple:point, PointOutsideBoard or None:exception ]
pointTests = []

# middle of board, should be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX // 2, tempY // 2
pointTests.append(["middle of board", (tempX, tempY), None])

# just inside board, should be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX -2, tempY -2
pointTests.append(["just inside of board", (tempX, tempY), None])

# on corner, should be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX -1, tempY -1
pointTests.append(["on corner of board", (tempX, tempY), None])

# just outside board, should NOT be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX-1, tempY
pointTests.append(["just outside of board Y", (tempX, tempY), PointOutsideBoard])

# just outside board, should NOT be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX, tempY -1
pointTests.append(["just outside of board X", (tempX, tempY), PointOutsideBoard])

# very outside board, should NOT be in range
tempX, tempY = generalTestBoardParams
tempX, tempY = tempX * 4, tempY * 4
pointTests.append(["very outside of board X", (tempX, tempY), PointOutsideBoard])


parentsAndPaths = [
	[{(8, 5): None, (7, 5): (8, 5), (6, 5): (7, 5), (5, 5): (6, 5), (6, 4): (6, 5), (4, 5): (5, 5), (5, 4): (5, 5), (3, 5): (4, 5), (4, 4): (4, 5), (4, 6): (4, 5), (4, 7): (4, 6)}, [(8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (4, 6), (4, 7)]],
	[{(3, 2): None, (4, 2): (3, 2), (5, 2): (4, 2), (6, 2): (5, 2), (5, 1): (5, 2), (5, 3): (5, 2), (5, 5): (5, 4), (4, 5): (5, 5), (6, 5): (5, 5), (7, 5): (6, 5), (8, 5): (7, 5), (4, 6): (4, 5), (4, 7): (4, 6), (5, 4): (5, 3)}, [(3, 2), (4, 2), (5, 2), (5, 3), (5, 4), (5, 5), (4, 5), (4, 6), (4, 7)]]
]


class TestRoomCreation(unittest.TestCase):
	@parameterized.expand([
		["small width", (minBoardSize, modestBoardSize)],
		["small height", (modestBoardSize, minBoardSize)],
		["both small", (minBoardSize, minBoardSize)],
		["modest sized", (modestBoardSize, modestBoardSize)]
	])
	def test_correct_board_creation(self, name, boardParams):
		b = Board(*boardParams)
		(width, height) = boardParams
		self.assertEqual(height, b.height)
		self.assertEqual(width, b.width)

		# all chars are set to "blocked" at first
		self.assertTrue(all(
			b._board[y][x] == charSet["blocked"]
			for y in range(b.height)
			for x in range(b.width)
		))

	def test_board_change_tile(self):
		b = Board(*generalTestBoardParams)
		point = (0, 0)
		charToChangeTo = charSet["start"]  # initial board is filled with 'blocked'

		# grab initial state of the char
		initialState = b._get_tile(point)

		# change state of position on board
		b._change_tile(point, charToChangeTo)

		# check the change took
		changedState = b._get_tile(point)

		self.assertNotEqual(initialState, changedState)
		self.assertEqual(changedState, charToChangeTo)

	@parameterized.expand(pointTests)
	def test_board_change_tile_range(self, name, point, exception):
		b = Board(*generalTestBoardParams)
		charToChangeTo = charSet["start"]  # initial board is filled with 'blocked'

		if exception is None:
			# change state of position on board
			b._change_tile(point, charToChangeTo)
		else:
			# equiv to "b._change_tile(point, charToChangeTo)"
			self.assertRaises(exception, b._change_tile, point, charToChangeTo)

	@parameterized.expand(pointTests)
	def test_board_get_tile_range(self, name, point, exception):
		b = Board(*generalTestBoardParams)
		charToChangeTo = charSet["start"]  # initial board is filled with 'blocked'
		if exception is None:
			# fetch state of position on board
			b._get_tile(point)
		else:
			# equiv to "b._get_tile(point)"
			self.assertRaises(exception, b._get_tile, point)

	@parameterized.expand(parentsAndPaths)
	def test_get_path(self, parent, expectedPath):
		'''
1st test:
````````````
`***````````
`**&````````
`***````````
````````***`
````````&**`
````````***`
```****`````
```****`````
```****`````
````````````
````````````

2nd test:
````````````
`***````````
`**&````````
`***````````
````````***`
````*******`
````*```***`
```*&**`````
```****`````
```****`````
````````````
````````````
		'''
		b = Board(*generalTestBoardParams)
		actualPath = b._get_path(parent, (4, 7))
		self.assertEqual(expectedPath, actualPath)

	@parameterized.expand(parentsAndPaths)
	def test_get_path_returns_blank_list(self, parent, expectedPath):
		# same parent settings as above test, but now we request a point that isn't in parent
		b = Board(*generalTestBoardParams)
		actualPath = b._get_path(parent, (15, 15))
		self.assertEqual([], actualPath) # should return an empty list

	def test_init_board_resets_all_params(self):
		def extract_params(board):
			return copy.deepcopy(board._board), copy.deepcopy(board._rooms), \
					copy.deepcopy(board._edges), copy.deepcopy(board._invalidNeighbors)

		def perturb(board):
			# make changes to internal data structures
			board._change_tile((0, 0), "|")
			board.add_room(Room(4, 4, 4, 4))
			board._add_edge((0, 0), (2, 2))
			board._invalidate((0, 0), (2, 2))

		b = Board(*generalTestBoardParams)
		initialParams = extract_params(b)

		# change the params
		perturb(b)
		adjustedParams = extract_params(b)

		# make sure all params have changed
		for init, adj in zip(initialParams, adjustedParams):
			self.assertNotEqual(init, adj)

		# reset params to initial state
		b.init_board()
		afterInitParams = extract_params(b)

		# make sure the initial params are restored
		for init, adj in zip(initialParams, afterInitParams):
			self.assertEqual(init, adj)


if __name__ == '__main__':
	unittest.main()
