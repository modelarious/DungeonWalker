import unittest

from generateMap import Board
from room import Room
from exceptions import *
from settings import *
from parameterized import parameterized

minBoardSize = MIN_BOARD_HEIGHT
modestBoardSize = minBoardSize * 12


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

	def test_board_(self, name, boardParams):
		pass
	
B = Board
B.
if __name__ == '__main__':
	unittest.main()