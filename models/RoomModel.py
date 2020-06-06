from exceptions import RoomTooSmall, RoomTooLarge
from settings import MIN_ROOM_HEIGHT, MIN_ROOM_WIDTH, MAX_ROOM_HEIGHT, MAX_ROOM_WIDTH
from heapq import heappush, heappop
from itertools import combinations


'''
exceptions that can be thrown:

# thrown when given room dimensions are too large
class RoomTooLarge(Exception):

# thrown when given room dimensions are too small
class RoomTooSmall(Exception):
'''
class RoomModel(object):
	#returns an empty string if the room bounds are within a valid 
	#range, otherwise returns a string describing the problem
	def roomWithinMinRange(self, height, width):
		if height < MIN_ROOM_HEIGHT:
			return self._getExceptionFormat(height, "height", MIN_ROOM_HEIGHT, "MIN_ROOM_HEIGHT", "<")
		if width < MIN_ROOM_WIDTH: 
			return self._getExceptionFormat(width, "width", MIN_ROOM_WIDTH, "MIN_ROOM_WIDTH", "<")
		return ""

	#returns an empty string if the room bounds are within a valid 
	#range, otherwise returns a string describing the problem
	def roomWithinMaxRange(self, height, width):
		if height > MAX_ROOM_HEIGHT: 
			return self._getExceptionFormat(height, "height", MAX_ROOM_HEIGHT, "MAX_ROOM_HEIGHT", ">")
		if width > MAX_ROOM_WIDTH:
			return self._getExceptionFormat(width, "width", MAX_ROOM_WIDTH, "MAX_ROOM_WIDTH", ">")
		return ""

	#produces a human readable representation of the values given to it
	#when called with (6, "width", 5, "MAX_ROOM_WIDTH", ">")
	#will produce "width (6) > MAX_ROOM_WIDTH (5)"
	def _getExceptionFormat(self, val1, val1Name, val2, val2Name, comparison):
		return f"{val1Name} ({val1}) {comparison} {val2Name} ({val2})"

	def __init__(self, height, width, topLeftX, topLeftY):

		#check if the room is too small
		notWithinMin = self.roomWithinMinRange(height, width)
		if notWithinMin: raise RoomTooSmall(notWithinMin)

		#check if the room is too large
		notWithinMax = self.roomWithinMaxRange(height, width)
		if notWithinMax: raise RoomTooLarge(notWithinMax)
		
		self.height = height
		self.width = width

		self.leftX = topLeftX
		self.rightX = topLeftX + width
		self.topY = topLeftY
		self.bottomY = topLeftY + height

		self.middleX = (self.leftX + self.rightX - 1) // 2
		self.middleY = (self.topY + self.bottomY - 1) // 2
		self.anchors = [
			(self.leftX, self.middleY),
			(self.rightX - 1, self.middleY),
			(self.middleX, self.topY),
			(self.middleX, self.bottomY -1)
		]

	#checks if there are any gaps between any edges on the boxes, 
	#if there aren't, then there is a collision
	def collide(self, otherRoom):
		conds = [self.leftX < otherRoom.rightX,
			self.rightX > otherRoom.leftX,
			self.topY < otherRoom.bottomY,
			self.bottomY > otherRoom.topY]
		return all(conds)

	def getAnchors(self):
		return self.anchors

	def __str__(self):
		return f"leftX = {self.leftX}, rightX = {self.rightX}, topY = {self.topY}, bottomY = {self.bottomY}"

