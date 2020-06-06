from settings import MIN_BOARD_WIDTH, MIN_BOARD_HEIGHT, charSet
from exceptions import * #BoardTooSmall
from heapq import heappush, heappop
from helpers.ManhattenDistance import manhatten_distance
import copy


class MapModel():
    def __init__(self, width, height, autoconnect):
        if width < MIN_BOARD_WIDTH or height < MIN_BOARD_HEIGHT: raise BoardTooSmall

        self.width = width
        self.height = height

        self._board = self._empty_board()
        self._rooms = []
        self._autoconnect = autoconnect


    def _empty_board(self):
        board = []
        for y in range(self.height):
            row = []
            #row = charSet["blocked"]*self.width
            
            for x in range(self.width):
                row.append(charSet["blocked"])
            board.append(row)
        return board

    # # set the board to a blank initial state
    # def init_board(self):
    #     board = []
    #     for y in range(self.height):
    #         row = []
    #         for x in range(self.width):
    #             row.append(charSet["blocked"])
    #         board.append(row)

    #     self._board = board
    #     self._rooms = []
    #     self._autoconnect = Autoconnect()

    def _get_tile(self, point):
        pX, pY = point
        if pX < 0 or pY < 0:
            raise PointOutsideBoard(
                f"get_tile: board width and height ({self.width}, {self.height}), given point: ({pX, pY})")
        try:
            return self._board[pY][pX]
        except IndexError:
            raise PointOutsideBoard(
                f"get_tile: board width and height ({self.width}, {self.height}), given point: ({pX, pY})")

    def _change_tile(self, point, char):
        pX, pY = point
        if pX < 0 or pY < 0:
            raise PointOutsideBoard(
                f"change_tile: board width and height ({self.width}, {self.height}), given point: ({pX, pY})")
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

        # add the room to the board visually
        for x in range(room.leftX, room.rightX):
            for y in range(room.topY, room.bottomY):
                point = (x, y)
                self._change_tile(point, charSet["passable"])

        # add the anchors visually
        for anchor in room.getAnchors():
            self._change_tile(anchor, charSet["anchor"])

        # track this room in autoconnect
        self._autoconnect.add_anchors(room)

        # track this room
        self._rooms.append(room)
        return True

    # used when you want to connect two anchors from two different graph components (ie two different rooms)
    # will first determine if the connection is possible using depth limited search
    # if the connection isn't possible, it returns false
    # if the connection is possible, it will add an edge between them and draw a path between the two anchors
    def connect_path_nodes(self, p1, p2):
        # no need to recompute this if we've already done it
        if self._autoconnect.have_edge(p1, p2):
            return True

        # Discover a path that connects the rooms using depth limited bfs... if you
        # find that these rooms can't be connected in the minimum number of moves (+ a little tolerance),
        # then return false
        path = self._depth_limited_search(p1, p2)
        if not path:
            return False
        else:
            self._autoconnect.add_edge(p1, p2)
            for node in path:
                self._change_tile(node, charSet["pathTemp"])
            return True

    def _point_in_board(self, pt):
        (pX, pY) = pt
        if pX < 0 or pY < 0:
            return False
        try:
            self._board[pY][pX]
            return True
        except IndexError:
            return False

    def _acceptable_char(self, pt):
        _acceptable_chars = [charSet[s] for s in ["anchor", "blocked", "pathTemp"]]
        if self._get_tile(pt) in _acceptable_chars:
            return True
        return False

    def _get_neighbors(self, currPoint):
        if self._point_in_board(currPoint):
            currX, currY = currPoint
            offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
            candidates = [(currX + offX, currY + offY) for offX, offY in offsets]
            candidates = list(filter(self._point_in_board, candidates))
            return candidates

        return []

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

        if not self._point_in_board(startPoint) or not self._point_in_board(endPoint):
            return False

        while len(openPoints) != 0:

            prio, currPoint = heappop(openPoints)
            done.append(currPoint)

            # we reached the end
            if currPoint == endPoint:
                break

            # get neighbors of current point
            neighbors = self._get_neighbors(currPoint)

            # code to make the path stay away from touching walls by 1 space
            neighbors_filtered = []
            for n in neighbors:
                if n == endPoint:
                    neighbors_filtered.append(n)
                    break

                # get neighbors of this neighbor
                #p1X, p1Y = n
                #nestedNeighborOffsets = [ x for x in product([-1, 0, 1], repeat=2) if x != (0, 0)] # XXX TODO want to check in a full 9 spaces around the point
                #tileAndNeighbors = [n] + [(p1X + offX, p1Y + offY) for offX, offY in nestedNeighborOffsets]
                tileAndNeighbors = [n] + self._get_neighbors(n)

                # if any are an unacceptable tile, skip this neighbor
                neighborTileUnacceptable = False
                for tile in tileAndNeighbors:
                    if not self._acceptable_char(tile):
                        neighborTileUnacceptable = True
                        break

                if neighborTileUnacceptable:
                    continue

                # neighbor passed all tests, so allow it
                neighbors_filtered.append(n)

            self._add_neighbors_to_heap(neighbors_filtered, openPoints, done, parent,
                                       cost, currPoint, endPoint, maxDepth)
        return self._get_path(parent, endPoint)

    # add all the neighbors that made it through filtering onto the priority queue for the next round of A*
    def _add_neighbors_to_heap(self, neighbors_filtered, openPoints, done, parent, cost, currPoint, endPoint, maxDepth):
        # look at all neighbors and add them to the heap
        for nbr in neighbors_filtered:
            if nbr not in done and self._point_in_board(nbr):
                updatedCost = cost[currPoint] + 1
                if nbr not in cost or updatedCost < cost[nbr]:
                    cost[nbr] = updatedCost
                    priority = updatedCost + manhatten_distance(*nbr, *endPoint)

                    # we don't want to search any deeper than "maxdepth"
                    if priority <= maxDepth:
                        heappush(openPoints, (priority, nbr))
                        parent[nbr] = currPoint

    def _get_path(self, parent, endPoint):
        if endPoint not in parent:
            return []

        # follow the path backwards and print it
        path = []
        p = parent[endPoint]
        path.append(endPoint)
        while p is not None:
            #print("Looking at ", p)
            path.append(p)
            p = parent[p]
        correctPath = [i for i in reversed(path)]
        return correctPath

    def _finalize_board(self):
        if len(self._rooms) == 0:
            return False
        StartRoom = self._rooms[0]
        GoalRoom, farthestPoint, pointInStartRoom = self._autoconnect.find_farthest_room(StartRoom)
        self._change_tile(farthestPoint, charSet["goal"])
        self._change_tile(pointInStartRoom, charSet["start"])
        return True

    def connect_board_automatically(self):
        if self._autoconnect.connect_graph(self):
            return self._finalize_board()
        return False

    def get_copy(self):
        return copy.deepcopy(self)

    def play_move(self, currentPosition, proposedPosition):
        tileToMove = self._get_tile(currentPosition)
        self._change_tile(proposedPosition,tileToMove)
        self._change_tile(currentPosition, charSet["passable"])








    # 3 rooms, each are their own strongly connected component
    # for a given anchor, it has 2 neighbors in this case: the closest anchor (that is not
    # invalid) from the other two rooms.  When you try to connect, you use _depth_limited_search() to see
    # if there's a path within reason that connects the two points.  If not, you invalidate those as neighbors.
    # You should be inspecting these pairs of anchors ordered by which two are the closest.
    # Each iteration you recalculate the connected components and re

    # NO TO THE ABOVE, Use Kruskal's algo.  So first, calculate the distance between each pair of anchors.  Don't use a pair that's invalidated


