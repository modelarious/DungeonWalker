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

from exceptions import *
from settings import *
from room import Room
from heapq import heappush, heappop
from itertools import combinations

'''
# thrown when a room given to the board would be outside the boundaries
class RoomOutsideBoard(Exception):

# thrown when a room given to the board collides with another room
class RoomCollision(Exception):

# thrown when the board dimensions are too small
class BoardTooSmall(Exception):
'''


class Board(object):
    def __init__(self, width, height):
        if width < MIN_BOARD_WIDTH or height < MIN_BOARD_HEIGHT: raise BoardTooSmall

        self.width = width
        self.height = height

        self._board = []
        self._rooms = []
        self._edges = dict()
        self._invalidNeighbors = dict()

        self.init_board()

    # set the board to a blank initial state
    def init_board(self):
        board = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(charSet["blocked"])
            board.append(row)

        self._board = board
        self._rooms = []
        self._edges = dict()
        self._invalidNeighbors = dict()

    # XXX I haven't acounted for negative values of x and y in the get tile or change tile
    def _get_tile(self, point):
        pX, pY = point
        try:
            return self._board[pY][pX]
        except IndexError:
            raise PointOutsideBoard(
                f"get_tile: board width and height ({self.width}, {self.height}), given point: ({pX, pY})")

    # XXX I haven't acounted for negative values of x and y in the get tile or change tile
    def _change_tile(self, point, char):
        pX, pY = point
        try:
            self._board[pY][pX] = char
        except IndexError:
            raise PointOutsideBoard(
                f"change_tile: board width and height ({self.width}, {self.height}), given point: ({pX, pY})")

    # print the board to the screen
    def draw_board(self):
        for row in self._board:
            print("".join(row).replace(charSet["pathTemp"], charSet["passable"]).replace(charSet["anchor"],
                                                                                         charSet["passable"]))
        print()

    def _room_is_outside_bounds(self, room):
        if room.rightX > self.width - 1:
            return f"room.rightX ({room.rightX}) > self.width - 1 ({self.width - 1})"
        if room.leftX < 1:
            return f"room.leftX ({room.leftX}) < 1"
        if room.bottomY > self.height - 1:
            return f"room.bottomY ({room.bottomY}) > self.height - 1 ({self.height - 1})"
        if room.topY < 1:
            return f"room.topY ({room.topY}) < 1"
        return ""

    # raises exceptions for cases where:
    # - the room would leave the bounds of the board
    # - the room would collide with another that already exists
    def add_room(self, room):

        # raise an exception if the rectangle would leave the bounds of the board
        outOfBounds = self._room_is_outside_bounds(room)
        if outOfBounds:
            raise RoomOutsideBoard(outOfBounds)

        # if the room would collide with another room that has already been placed
        if any(room.collide(placedRoom) for placedRoom in self._rooms):
            raise RoomCollision

        # add the room to the board
        for x in range(room.leftX, room.rightX):
            for y in range(room.topY, room.bottomY):
                point = (x, y)
                self._change_tile(point, charSet["passable"])

        self._add_anchors(room)

        # track this room
        self._rooms.append(room)
        return True

    def _add_anchors(self, room):
        # connect the anchors in the edge list to make the room a strongly connected component
        anchors = room.getAnchors()
        for anchor1, anchor2 in combinations(anchors, 2):
            anchor1x, anchor1y = anchor1
            anchor2x, anchor2y = anchor2
            self._add_edge(anchor1, anchor2)

        # add the anchors visually
        for anchor in room.getAnchors():
            self._change_tile(anchor, charSet["anchor"])

    # used when you want to connect two anchors from two different graph components (ie two different rooms)
    # will first determine if the connection is possible using depth limited search
    # if the connection isn't possible, it will invalidate future connections between these sets of points
    # if the connection is possible, it will add an edge between them and draw a path between the two anchors
    def connect_path_nodes(self, p1, p2):
        # Actually connect the rooms using depth limited bfs... if you find that these rooms can't be connected in
        # the minimum number of moves, then invalidate this set of points
        path = self._depth_limited_search(p1, p2)

        # XXX invalidate the set of points for autoconnect feature
        if not path:
            return False
        else:
            self._add_edge(p1, p2)
            for node in path:
                self._change_tile(node, charSet["pathTemp"])
            return True

    def _search_path(self, tile, endPoint):
        offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
        q = []
        seen = []
        parent = {}

        q.append(tile)
        parent[tile] = None

        while len(q) != 0:
            point = q.pop()

            if point in seen:
                continue

            if point == endPoint:
                break

            seen.append(point)
            pX, pY = point
            neighbors = [(pX + offX, pY + offY) for offX, offY in offsets]

            # only include neighbors that are part of an existing path, as we are serching down a path
            filteredNeighbors = [n for n in neighbors if self._get_tile(n) == charSet["pathTemp"]]
            for n in filteredNeighbors:
                if n not in seen:
                    q.append(n)
                    parent[n] = point

        return self._get_path(parent, endPoint), parent

    '''
defines the a star algorithm from "startPoint" to "endPoint", where the heuristic is
manhatten_distance. Depth is limited by the cost already paid to reach a point.
    '''

    def _depth_limited_search(self, startPoint, endPoint):

        # a little bit of tolerance allowing for up to 10 extra spaces to get around unexpected objects
        maxDepth = manhatten_distance(*startPoint, *endPoint) + 10

        # first element in open list is the start point
        openPoints = []
        heappush(openPoints, (0, startPoint))

        parent, cost, done = {}, {}, []
        parent[startPoint] = None
        cost[startPoint] = 0

        while len(openPoints) != 0:

            prio, currPoint = heappop(openPoints)
            done.append(currPoint)
            if currPoint == endPoint: break

            # get neighbors of current point
            currX, currY = currPoint
            offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
            neighbors = [(currX + offX, currY + offY) for offX, offY in offsets]

            # code to make the path stay away from touching walls by 1 space
            # also checks for existing temporary paths that would be able to join to our target that we could follow
            neighbors_filtered = []
            acceptable_chars = [charSet[s] for s in ["anchor", "blocked", "pathTemp"]]
            for n in neighbors:
                if n == endPoint:
                    neighbors_filtered.append(n)
                    break

                # get neighbors of this neighbor
                p1X, p1Y = n
                tileAndNeighbors = [n] + [(p1X + offX, p1Y + offY) for offX, offY in offsets]

                # if any are an unacceptable tile, skip this neighbor
                neighborTileUnacceptable = False
                for tile in tileAndNeighbors:
                    tileChar = self._get_tile(tile)
                    if tileChar not in acceptable_chars:
                        neighborTileUnacceptable = True
                        break

                    if tileChar == charSet["pathTemp"]:
                        path, parents = self._search_path(tile, endPoint)
                        if path:
                            parents[tile] = n
                            parents[n] = currPoint
                            parent.update(parents)
                            return self._get_path(parent, endPoint)

                if neighborTileUnacceptable:
                    continue

                # neighbor passed all tests, so allow it
                neighbors_filtered.append(n)

            # look at all neighbors and add them to the heap
            for nbr in neighbors_filtered:
                if nbr not in done:
                    updatedCost = cost[currPoint] + 1
                    if nbr not in cost or updatedCost < cost[nbr]:
                        cost[nbr] = updatedCost
                        priority = updatedCost + manhatten_distance(*nbr, *endPoint)

                        # we don't want to search any deeper than "maxdepth"
                        if priority <= maxDepth:
                            heappush(openPoints, (priority, nbr))
                            parent[nbr] = currPoint

        return self._get_path(parent, endPoint)

    def _get_path(self, parent, endPoint):
        if endPoint not in parent:
            return []

        # follow the path backwards and print it
        path = []
        p = parent[endPoint]
        path.append(endPoint)
        while p is not None:
            path.append(p)
            p = parent[p]
        correctPath = [i for i in reversed(path)]
        return correctPath




    def __cross_connect(self, p1, p2, d):
        # partner function with __check_with_keyerror, we store True at d[p1][p2]
        if p1 not in d:
            d[p1] = dict()
        if p2 not in d:
            d[p2] = dict()

        d[p1][p2] = True
        d[p2][p1] = True

    def __check_with_keyerror(self, p1, p2, d):
        # partner function with __cross_connect, we store True at d[p1][p2]
        # returns true if d[p1][p2] exists, false if no
        try:
            return d[p1][p2]
        except KeyError:
            return False

    # going to be used for autoconnect feature, so not tested yet
    def _add_edge(self, p1, p2):
        self.__cross_connect(p1, p2, self._edges)

    def _have_edge(self, p1, p2):
        return self.__check_with_keyerror(p1, p2, self._edges)

    def _invalidate(self, p1, p2):
        self.__cross_connect(p1, p2, self._invalidNeighbors)

    def _points_are_invalid(self, p1, p2):
        return self.__check_with_keyerror(p1, p2, self._invalidNeighbors)

    # going to be used for autoconnect feature, so not tested yet
    def _get_neighbors(self, point):
        try:
            return self._edges[point]
        except KeyError:
            return False

    # 3 rooms, each are their own strongly connected component
    # for a given anchor, it has 2 neighbors in this case: the closest anchor (that is not
    # invalid) from the other two rooms.  When you try to connect, you use _depth_limited_search() to see
    # if there's a path within reason that connects the two points.  If not, you invalidate those as neighbors.
    # You should be inspecting these pairs of anchors ordered by which two are the closest.
    # Each iteration you recalculate the connected components and re

    # NO TO THE ABOVE, Use Kruskal's algo.  So first, calculate the distance between each pair of anchors.  Don't use a pair


def manhatten_distance(p1X, p1Y, p2X, p2Y):
    return abs(p1X - p2X) + abs(p1Y - p2Y)


if __name__ == '__main__':
    b = Board(12, 12)

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

    b.add_room(Room(3, 3, 1, 1))
    b.add_room(Room(3, 3, 8, 4))
    b.add_room(Room(3, 4, 3, 7))
    '''
roomHeight, roomWidth = (4, 5)
topLeftX, topLeftY = (3,1)

r = Room(roomHeight, roomWidth, topLeftX, topLeftY)
x.add_room(r)

x.add_room(r)
    '''

    b.draw_board()

    p1 = (8, 5)
    # p1 = (3, 2)
    p2 = (4, 7)
    b.connect_path_nodes(p1, p2)
    b.draw_board()
    p1 = (3, 2)
    # p1 = (8, 5)
    b.connect_path_nodes(p1, p2)

    b.draw_board()
    print(b._edges)
