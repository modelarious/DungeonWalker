import unittest

from generateMap import Room
from exceptions import *
from parameterized import parameterized

#max Room Size and min Room Size
maxRS = 10
minRS = 2
medianRS = 5
class TestRoomCreation(unittest.TestCase):

	@parameterized.expand([
		["boundarySmallHeight",         (minRS, medianRS, 0, 0)],
		["boundarySmallWidth",          (medianRS, minRS, 0, 0)],
		["boundarySmallWidthAndHeight", (minRS, minRS, 0, 0)],
		["boundaryLargeHeight",         (maxRS, medianRS, 0, 0)],
		["boundaryLargeWidth",          (medianRS, maxRS, 0, 0)],
		["boundaryLargeWidthAndHeight", (maxRS, maxRS, 0, 0)],
	])
	def test_correct_room_creation(self, name, roomParams):
		r = Room(*roomParams)
		(height, width, _, _) = roomParams
		self.assertEqual(height, r.height)
		self.assertEqual(width, r.width)

	@parameterized.expand([
		["roomTooSmallHeight", (minRS-1, medianRS, 0, 0), RoomTooSmall],
		["roomTooSmallWidth", (medianRS, minRS-1, 0, 0), RoomTooSmall],
		["roomTooSmallWidthAndHeight", (minRS-1, minRS-1, 0, 0), RoomTooSmall],
		["roomTooLargeHeight", (maxRS+1, medianRS, 0, 0), RoomTooLarge],
		["roomTooLargeWidth",          (medianRS, maxRS+1, 0, 0), RoomTooLarge],
		["roomTooLargeWidthAndHeight", (maxRS+1, maxRS+1, 0, 0), RoomTooLarge],
	])
	def test_room_creation_exceptions(self, name, roomParams, exception):
		self.assertRaises(exception, Room, *roomParams)


if __name__ == '__main__':
    unittest.main()

