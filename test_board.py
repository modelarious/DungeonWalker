import unittest

from generateMap import Board
from room import Room
from exceptions import *
from settings import *
from parameterized import parameterized

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

if __name__ == '__main__':
	unittest.main()
