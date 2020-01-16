import unittest

from generateMap import Board
from room import Room
from exceptions import *
from settings import *
from parameterized import parameterized

minBoardSize = MIN_BOARD_HEIGHT
modestBoardSize = minBoardSize * 4

generalTestBoardParams = (modestBoardSize, modestBoardSize - 3)


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
		x, y = point
		charToChangeTo = charSet["start"]  # initial board is filled with 'blocked'

		# grab initial state of the char
		initialState = b._get_tile(point)

		# change state of position on board
		b._change_tile(x, y, charSet['start'])

		# check the change took
		changedState = b._get_tile(point)

		self.assertNotEqual(initialState, changedState)
		self.assertEqual(changedState, charToChangeTo)

	def test_board_change_tile_outside_range(self):
		b = Board(*generalTestBoardParams)

		# get the far edge of the board, and multiply the width by 4
		x, y = generalTestBoardParams
		x *= 4
		charToChangeTo = charSet["start"]  # initial board is filled with 'blocked'

		# equiv to "b._change_tile(x, y, charToChangeTo)"
		self.assertRaises(PointOutsideBoard, b._change_tile, x, y, charToChangeTo)


if __name__ == '__main__':
	unittest.main()
