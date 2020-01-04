'''
Steps:
1) place a few rooms
ex:
`````````````
`***`````````
`***`````````
`***`````***`
`````````***`
`````````***`
`````````````
```****``````
```****``````
```****``````
`````````````

smallest possible map:
````
`GS`
`**`
````

some rules:
	- can't place a room such that one of its walls is on the edge of the map (1 space buffer around entire map)
	- can't place two rooms such that their walls touch
	
2) generate a graph where each room exit is a node (there are 4 room exits, 
	each on the center of a room's wall)
ex:
`````
`***`
`***`
`***`
`````

has 4 exits (marked by the & symbol):
`````
`*&*`
`&*&`
`*&*`
`````
 
3) connect the rooms using either
	- prim's algorithm
	- iteratively randomly connecting rooms until a dfs can reach every room

4) place the start and goal in random rooms
'''
charSet = {
	"blocked" : "`",
	"passable" : "*",
	"Start" : "S",
	"Goal" : "G",
#       "Treasure" : "T",
#       "Lava" : "L"
}

# thrown when given room dimensions are too large
class RoomTooLarge(Exception):
	pass

# thrown when given room dimensions are too small
class RoomTooSmall(Exception):
	pass

# thrown when a room given to the board would be outside the boundaries
class RoomOutsideBoard(Exception):
	pass

# thrown when a room given to the board collides with another room
class RoomCollision(Exception):
	pass

# thrown when the board 
class BoardTooSmall(Exception):
	pass


class Room(object):
	MAX_ROOM_HEIGHT = 10
	MAX_ROOM_WIDTH = 10
	MIN_ROOM_WIDTH = 2
	MIN_ROOM_HEIGHT = 2

	def __init__(self, height, width, topLeftX, topLeftY):

		#check if the room is too large
		if height > Room.MAX_ROOM_HEIGHT: raise RoomTooLarge
		if width > Room.MAX_ROOM_WIDTH: raise RoomTooLarge

		#check if the room is too small
		if height < Room.MIN_ROOM_HEIGHT: raise RoomTooSmall
		if width < Room.MIN_ROOM_WIDTH: raise RoomTooSmall

		self.height = height
		self.width = width

		self.leftX = topLeftX
		self.rightX = topLeftX + width
		self.topY = topLeftY
		self.bottomY = topLeftY + height


	#checks if there are any gaps between any edges on the boxes, 
	#if there aren't, then there is a collision
	def collide(self, otherRoom):
		conds = [self.leftX < otherRoom.rightX,
			self.rightX > otherRoom.leftX,
			self.topY < otherRoom.bottomY,
			self.bottomY > otherRoom.topY]
		return all(conds)

	def __str__(self):
		return f"leftX = {self.leftX}, rightX = {self.rightX}, topY = {self.topY}, bottomY = {self.bottomY}"


class Board(object):
	def __init__(self, width, height):
		if width < 4 or height < 4: raise BoardTooSmall

		self.width = width
		self.height = height
		self.board = []
		self.rooms = []
		
		self.initBoard()
		self.drawBoard()

	#set the board to a blank initial state
	def initBoard(self):
		board = []
		for y in range(self.height):
			row = []
			for x in range(self.width):
				row.append(charSet["blocked"])
			board.append(row)
		self.board = board

	#print the board to the screen
	def drawBoard(self):
		for row in self.board:
			print("".join(row))
		print()
	
	#raises exceptions for cases where:
	#	- the room would leave the bounds of the board
	#	- the room would collide with another that already exists
	def addRoom(self, room):

		#if the rectangle would leave the bounds of the board
		if room.rightX > self.width - 1 or room.leftX < 1 or room.bottomY > self.height -1 or room.topY < 1:
			raise RoomOutsideBoard

		#if the room would collide with another that has already been placed
		if any(room.collide(placedRoom) for placedRoom in self.rooms):
			raise RoomCollision

		for x in range(room.leftX, room.rightX):
			for y in range(room.topY, room.bottomY):	
				self.board[y][x] = charSet["passable"]

		self.rooms.append(room)
		return True



# thrown when a room given to the board would be outside the boundaries
class RoomOutsideBoard(Exception):
        pass

# thrown when a room given to the board collides with another room
class RoomCollision(Exception):
        pass

# thrown when the board
class BoardTooSmall(Exception):
        pass	
x = Board(12, 12)

'''
`````````````
`***`````````
`***`````````
`***`````***`
`````````***`
`````````***`
`````````````
```****``````
```****``````
```****``````
`````````````
'''

x.addRoom(Room(3, 3, 1, 1))
x.addRoom(Room(3, 3, 8, 4))
x.addRoom(Room(3, 4, 3, 7))
'''
roomHeight, roomWidth = (4, 5)
topLeftX, topLeftY = (3,1)

r = Room(roomHeight, roomWidth, topLeftX, topLeftY)
x.addRoom(r)

x.addRoom(r)
'''
x.drawBoard()


