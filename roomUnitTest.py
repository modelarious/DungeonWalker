import unittest

#from generateMap import Board
from room import Room
from exceptions import *
from settings import *
from parameterized import parameterized

#max, min and median Room Size
maxRS = MAX_ROOM_HEIGHT
minRS = MIN_ROOM_HEIGHT
medianRS = (maxRS + minRS) // 2

evenValidRoomSize = 6
oddValidRoomSize = 7

'''
[(0, 2), (5, 2), (2, 0), (2, 5)]
[(0, 3), (5, 3), (2, 0), (2, 6)]
.[(0, 2), (6, 2), (3, 0), (3, 5)]
.[(0, 3), (6, 3), (3, 0), (3, 6)]
'''

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


	@parameterized.expand([
		["EvenWidthAndHeight", (evenValidRoomSize, evenValidRoomSize, 1, 1), [(1, 3), (6, 3), (3, 1), (3, 6)]],
		["EvenWidthOddHeight", (oddValidRoomSize, evenValidRoomSize, 1, 1), [(1, 4), (6, 4), (3, 1), (3, 7)]],
		["OddWidthEvenHeight", (evenValidRoomSize, oddValidRoomSize, 1, 1), [(1, 3), (7, 3), (4, 1), (4, 6)]],
		["OddWidthOddHeight", (oddValidRoomSize, oddValidRoomSize, 1, 1), [(1, 4), (7, 4), (4, 1), (4, 7)]],
		["min sized room", (minRS, minRS, 1, 1), [(1, 2), (3, 2), (2, 1), (2, 3)]]
	])
	def test_anchors_in_correct_locations(self, name, roomParams, expectedAnchors):
		r = Room(*roomParams)
		self.assertEqual(r.getAnchors(), expectedAnchors)

	@parameterized.expand([
		["Room 2 equals Room 1", Room(5, 5, 1, 1), Room(5, 5, 1, 1)],
		["Room 2 inside Room 1", Room(maxRS, maxRS, 1, 1), Room(minRS, minRS, medianRS, medianRS)],
		["Room 2 top left corner in Room 1", Room(5, 5, 1, 1), Room(5, 5, 2, 2)],
		["Room 2 top left corner barely in Room 1", Room(5, 5, 1, 1), Room(5, 5, 5, 5)],
		["Room 2 top right corner in Room 1", Room(5, 5, 2, 1), Room(5, 5, 1, 2)],
		["Room 2 top right corner barely in Room 1", Room(5, 5, 5, 1), Room(5, 5, 1, 5)],
		["Room 2 taller than Room 1, no corners inside of each (form a cross)", Room(3, 7, 3, 3), Room(7, 3, 5, 1)]
	])
	def test_rooms_collide(self, name, room1, room2):
	#	b = Board(12, 12)
	#	b.addRoom(room1)
	#	b.addRoom(room2)
	#	b.drawBoard()
		self.assertTrue(room1.collide(room2))
		self.assertTrue(room2.collide(room1))

	@parameterized.expand([
		["Room 2 borders Room 1 on the side", Room(3, 3, 1, 1), Room(3, 3, 4, 1)],
		["Room 2 borders Room 1 on the bottom", Room(3, 3, 1, 1), Room(3, 3, 1, 4)],
		["Rooms are nowhere close", Room(3, 3, 1, 1), Room(3, 3, 15, 15)]
	])
	def test_rooms_dont_collide(self, name, room1, room2):
	#	b = Board(30, 30)
	#	b.addRoom(room1)
	#	b.addRoom(room2)
	#	b.drawBoard()
		self.assertFalse(room1.collide(room2))
		self.assertFalse(room2.collide(room1))

	def test_string_representation(self):
		shift = 3
		r = Room(medianRS, medianRS, shift, shift)
		self.assertEqual(f"leftX = {shift}, rightX = {medianRS+shift}, topY = {shift}, bottomY = {medianRS+shift}", r.__str__())
if __name__ == '__main__':
    unittest.main()

