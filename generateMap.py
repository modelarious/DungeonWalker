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



from heapq import heappush, heappop
from itertools import combinations

charSet = {
	"blocked" : "`",
	"passable" : "*",
	"start" : "S",
	"goal" : "G",
	"anchor" : "&",
	"player" : "@",
	"pathTemp" : "-",
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


class Board(object):
	def __init__(self, width, height):
		if width < 4 or height < 4: raise BoardTooSmall

		self.width = width
		self.height = height
		self.board = []
		self.rooms = []
		self.edges = dict()
		
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

	def changeTile(self, x, y, char):
		self.board[y][x] = char

	#print the board to the screen
	def drawBoard(self):
		for row in self.board:
			print("".join(row).replace(charSet["pathTemp"], charSet["passable"]).replace(charSet["anchor"], charSet["passable"]))
		print()
	
	#raises exceptions for cases where:
	#	- the room would leave the bounds of the board
	#	- the room would collide with another that already exists
	def addRoom(self, room):

		#if the rectangle would leave the bounds of the board
		if room.rightX > self.width - 1 or room.leftX < 1 or room.bottomY > self.height -1 or room.topY < 1:
			raise RoomOutsideBoard

		#if the room would collide with another room that has already been placed
		if any(room.collide(placedRoom) for placedRoom in self.rooms):
			raise RoomCollision

		#add the room to the board
		for x in range(room.leftX, room.rightX):
			for y in range(room.topY, room.bottomY):
				self.changeTile(x, y, charSet["passable"])	

		self.drawBoard()
		self._addAnchors(room)

		#track this room
		self.rooms.append(room)
		return True

	def _addAnchors(self, room):
		#connect the anchors in the edge list to make the room a strongly connected component
		self._addRoomNodes(room)
		
		#add the anchors visually
		for x, y in room.getAnchors():
			self.changeTile(x, y, charSet["anchor"])

	def _connectRoomPoints(self, p1, p2):
		self._addEdge(p1, p2)

	def _addEdge(self, p1, p2):
		#sort based on the first coordinate, breaking ties with the second coordinate.
		#this is so that I don't have to memoize both (p1, p2) and (p2, p1) as they will
		#always be in the same order after the sort step
		_p1, _p2 = sorted((p1,p2))
		if _p1 not in self.edges:
			self.edges[_p1] = dict()

		self.edges[_p1][_p2] = True

		return True	

	def _addRoomNodes(self, room):
		anchors = room.getAnchors()
		for anchor1, anchor2 in combinations(anchors, 2):
			anchor1x, anchor1y = anchor1
			anchor2x, anchor2y = anchor2
			print(manhatten_distance(*anchor1, *anchor2))
			print(anchor1x, anchor1y, anchor2x, anchor2y)
			self._connectRoomPoints(anchor1, anchor2)
		print(self.edges)
	
	#used when you want to connect two anchors from two different graph components (ie two different rooms)
	#will first determine if the connection is possible using depth limited search
	#if the connection isn't possible, it will invalidate future connections between these sets of points
	#if the connection is possible, it will add an edge between them and draw a path between the two anchors
	def _connectPathNodes(self, p1, p2):
		print(f"Connecting {p1} and {p2}")
		#Actually connect the rooms using depth limited bfs... if you find that these rooms can't be connected in the minimum number of moves, then invalidate this set of points
		path = self._depthLimitedSearch(p1, p2)

		#XXX invalidate the set of points
		if path == []:
			pass
		else:
			self._addEdge(p1, p2)

		for x, y in path:
			self.changeTile(x, y, charSet["pathTemp"])

	def _searchPath(self, tile, endPoint):
		print("\nEnter search path")
		offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
		q = []
		seen = []
		parent = {}
		
		q.append(tile)
		parent[tile] = None

		while len(q) != 0:
			point = q.pop()

			print(f"looking at point {point}, seen={seen}")
			if point in seen:
				continue

			if point == endPoint:
				print("WHOA")
				break

			seen.append(point)
			pX, pY = point
			neighbors = [(pX + offX, pY + offY) for offX, offY in offsets]

			print(f"neighbors of {point} are {neighbors}")
			#only include neighbors that are part of an existing path, as we are serching down a path
			filteredNeighbors = [n for n in neighbors if self.get_tile(n) == charSet["pathTemp"]]
			print(f"neighbors of {point} are {filteredNeighbors}")
			for n in filteredNeighbors:
				if n not in seen:
					q.append(n)
					parent[n] = point

#		return self.print_path(parent, endPoint), parent
		print(parent)
		#follow the path backwards and print it
		path = []
		p = parent[endPoint] #XXX Unsafe operation, don't assume the path was formed (maybe use .setdefault())
		path.append(endPoint)
		while p != None:
			path.append(p)
			p = parent[p]
		correctPath = [i for i in reversed(path)]
		print(correctPath)
		return correctPath, parent
			
		
	'''
defines the a star algorithm from "startPoint" to "endPoint", where the heuristic is
manhatten_distance. Depth is limited by the cost already paid to reach a point.
	'''
	def _depthLimitedSearch(self, startPoint, endPoint):

		#a little bit of tolerance allowing for up to 10 extra spaces to get around unexpected objects
		maxDepth = manhatten_distance(*startPoint, *endPoint) + 10
		
		#first element in open list is the start point
		openPoints = []
		heappush(openPoints, (0, startPoint))
		
		parent, cost, done = {}, {}, []
		parent[startPoint] = None
		cost[startPoint] = 0

		while len(openPoints) != 0:

			prio, currPoint = heappop(openPoints)
			done.append(currPoint)
			if currPoint == endPoint: break

			#get neighbors of current point
			currX, currY = currPoint
			offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
			neighbors = [(currX + offX, currY + offY) for offX, offY in offsets]


			#code to make the path stay away from touching walls by 1 space
			#XXX also checks for existing temporary paths that would be able to join to our target that we could follow
			neighbors_filtered = []
			acceptable_chars = [charSet[s] for s in ["anchor", "blocked", "pathTemp"]]
			for n in neighbors:
				if n == endPoint:
					neighbors_filtered.append(n)
					break

				#get neighbors of this neighbor
				p1X, p1Y = n
				tileAndNeighbors = [n] + [(p1X + offX, p1Y + offY) for offX, offY in offsets]
				
				#if any are an unacceptable tile, skip this neighbor
				neighborTileUnacceptable = False
				for tile in tileAndNeighbors:
					tileChar = self.get_tile(tile)
					if tileChar not in acceptable_chars:
						neighborTileUnacceptable = True
						break
					
					if tileChar == charSet["pathTemp"]:
						path, parents = self._searchPath(tile, endPoint)
						if path != []:
							parents[tile] = n
							parents[n] = currPoint
							parent.update(parents)
							return self.print_path(parent, endPoint)
					
				if neighborTileUnacceptable == True:
					continue

				#neighbor passed all tests, so allow it
				neighbors_filtered.append(n)

			#look at all neighbors and add them to the heap
			for nbr in neighbors_filtered:
				if nbr not in done:
					print(f"Looking at {nbr},  distance = {manhatten_distance(*nbr, *endPoint)}")
					updatedCost = cost[currPoint] + 1
					if nbr not in cost or updatedCost < cost[nbr]:
						cost[nbr] = updatedCost
						priority = updatedCost + manhatten_distance(*nbr, *endPoint)

						#we don't want to search any deeper than "maxdepth"
						if priority <= maxDepth:
							heappush(openPoints, (priority, nbr))
							parent[nbr] = currPoint

		return self.print_path(parent, endPoint)

	def print_path(self, parent, endPoint):
		#follow the path backwards and print it
		path = []
		p = parent[endPoint] #XXX Unsafe operation, don't assume the path was formed (maybe use .setdefault())
		path.append(endPoint)
		while p != None:
			path.append(p)
			p = parent[p]
		correctPath = [i for i in reversed(path)]
		print(correctPath)
		return correctPath

	def get_tile(self, point):
		pX, pY = point
		return self.board[pY][pX] #XXX THIS IS PRONE TO ERROR, PLEASE MAKE SURE TO CHECK THIS!!

def manhatten_distance(p1X, p1Y, p2X, p2Y):
	return abs(p1X - p2X) + abs(p1Y - p2Y)


x = Board(12, 12)

'''
`````````````
`*&*`````````
`&*&`````````
`*&*`````*&*`
`````````&*&`
`````````*&*`
`````````````
```*&**``````
```&**&``````
```*&**``````
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

p1 = (8, 5)
p2 = (4, 7)
x._connectPathNodes(p1, p2)
x.drawBoard()
p1 = (3, 2)
x._connectPathNodes(p1, p2)

x.drawBoard()


