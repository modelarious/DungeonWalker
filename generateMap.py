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

class Room(object):
	def __init__(self, height, width, topLeftX, topLeftY):
		self.height = height
		self.width = width
		self.topLeftX = topLeftX
		self.topLeftY = topLeftY


		#self.bottomRightX = topLeftX + 
		
class Board(object):
	def __init__(self, width, height):
		assert width >= 4, f"Width must be 4 or greater, not {width}"
		assert height >= 4, f"Height must be 4 or greater, not {height}"

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
		print(board)
		self.board = board

	#print the board to the screen
	def drawBoard(self):
		for row in self.board:
			print("".join(row))
		print()
	
	#returns False on failure:
	#	- height or width were less than 2
	#	- top left X or top left Y were less than 1
	#returns True on success
	def addRoom(self, room):
		#if height or width are < 2 or the 
		#top left coordinates are < 1, return false
		if room.height < 2 or room.width < 2 or room.topLeftX < 1 or room.topLeftY < 1:
			return False

		#XXX if the rectangle would go out of bounds on the board

		#XXX if the room would collide with another

		for x in range(room.topLeftX, room.topLeftX + room.width):
			for y in range(room.topLeftY, room.topLeftY + room.height):	
				self.board[y][x] = charSet["passable"]

		return True
	
x = Board(12, 12)

roomHeight, roomWidth = (3, 4)
topLeftX, topLeftY = (3,1)

r = Room(roomHeight, roomWidth, topLeftX, topLeftY)
x.addRoom(r)
x.drawBoard()


