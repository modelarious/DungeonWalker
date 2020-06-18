import unittest

from models.MapModel import MapModel as Board
from models.RoomModel import RoomModel as Room
from controllers.AdditionController import AdditionController
from exceptions import *
from settings import *
from parameterized import parameterized
from TestingFixtures import *

# use the boundary setting from the addition controller
b = Board(*generalTestBoardParams)
ac = AdditionController(b)
boundary = ac.boundarySize

(rHeight, rWidth)  = generalRoomSize

# array of entries of form [String:name, Int:x, Int:y, RoomOutsideBoard or None:exception]
RoomPlacements = [
		["X is too small", 0, boundary, RoomOutsideBoard],
		["Y is too small", boundary, 0, RoomOutsideBoard],
		["X and Y are too small", 0, 0, RoomOutsideBoard],
		["X and Y are just within bounds on the top left", boundary, boundary, None],
		["Y is just within bounds on the bottom left", boundary, generalTestBoardY - (rHeight + boundary), None],
		["X is just within bounds on the top right", generalTestBoardX - (rWidth + boundary), boundary, None],
		["X and Y are just within bounds on the bottom right", generalTestBoardX - (rWidth + boundary), generalTestBoardY - (rHeight + boundary), None],
		["Y is just outside bounds on the bottom left", boundary, generalTestBoardY - (rHeight + boundary - 1), RoomOutsideBoard],
		["X is just outside bounds on the top right", generalTestBoardX - (rWidth + boundary - 1), boundary, RoomOutsideBoard],
		["X and Y are just outside bounds on the bottom right", generalTestBoardX - (rWidth + boundary - 1), generalTestBoardY - (rHeight + boundary - 1), RoomOutsideBoard]
]

class TestBoardCreation(unittest.TestCase):

	@parameterized.expand(RoomPlacements)
	def test_room_is_outside_bounds(self, name, x, y, exception):
		b = Board(*generalTestBoardParams)
		room = Room(*generalRoomSize, x, y)
		additionController = AdditionController(b)

		if exception:
			self.assertRaises(exception, additionController.add_room, room)
		else:
			additionController.add_room(room)
	

	# XXX this is a pitiful amount of testing for this function
	def test_get_neighbors_returns_empty_list(self):
		b = Board(*generalTestBoardParams)
		additionController = AdditionController(b)
		self.assertEqual([], additionController.get_neighbors((300, 300)))