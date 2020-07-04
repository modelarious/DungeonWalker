from exceptions import RoomCollision
from settings import charSet
from helpers.ManhattenDistance import manhatten_distance
from heapq import heappush, heappop
from copy import deepcopy


class MapGeneratorEngine():
    def __init__(self, autoconnect, additionController):
        self.additionController = additionController
        self.autoconnect = autoconnect
        self.rooms = []
        self.enemySpawnPoints = []

    # raises exceptions for cases where:
    # - the room would leave the bounds of the board
    # - the room would collide with another that already exists
    def add_room(self, room):

        # if the room would collide with another room that has already been placed
        if any(room.collide(placedRoom) for placedRoom in self.rooms):
            raise RoomCollision
            
        # ask the controller to add the room to the board
        self.additionController.add_room(room)

        # track this room in the graph
        self.autoconnect.add_anchors(room)

        # track this room for collision checks
        self.rooms.append(room)

        self.enemySpawnPoints.extend(room.generate_spawn_points())
    
    def get_spawn_points(self):
        return self.enemySpawnPoints

    # used when you want to connect two anchors from two different graph components (ie two different rooms)
    # will first determine if the connection is possible using depth limited search
    # if the connection isn't possible, it returns false
    # if the connection is possible, it will add an edge between them and draw a path between the two anchors
    # XXX This stuff should go into the AdditionController.. also rename the AdditionController, maybe MapAdditionController, MapFeatureAdditionController?
    # XXX anything that handles rooms should be in this engine, everything else should go in the AdditionController?
    def connect_path_nodes(self, p1, p2):
        # no need to recompute this if we've already done it
        if self.autoconnect.have_edge(p1, p2):
            # print("returning early as we've already done this shit!")
            return True

        # Discover a path that connects the rooms using depth limited bfs... if you
        # find that these rooms can't be connected in the minimum number of moves (+ a little tolerance),
        # then return false
        path = self._depth_limited_search(p1, p2)
        if not path:
            # print("didn't work")
            return False
        else:
            self.autoconnect.add_edge(p1, p2)
            self.additionController.add_path(path)
            # print("connected up the path and all that")
            return True

    def _acceptable_char(self, pt):
        _acceptable_chars = [charSet[s] for s in ["anchor", "blocked", "pathTemp"]] #XXX this is bad!! these should be constants if you reference them like this
        if self.additionController.get_point(pt) in _acceptable_chars:
            return True
        return False

    '''
    defines the a star algorithm from "startPoint" to "endPoint", where the heuristic is
    manhatten_distance. Depth is limited by the cost already paid to reach a point.
    '''
    def _depth_limited_search(self, startPoint, endPoint):
        # a little bit of tolerance allowing for up to 50 extra spaces to get around unexpected objects
        maxDepth = manhatten_distance(*startPoint, *endPoint) + 50

        # first element in open list is the start point
        openPoints = []
        heappush(openPoints, (0, startPoint))

        parent, cost, done = {}, {}, []
        parent[startPoint] = None
        cost[startPoint] = 0

        if not self.additionController.point_in_board(startPoint) or not self.additionController.point_in_board(endPoint):
            return False

        while len(openPoints) != 0:

            prio, currPoint = heappop(openPoints)
            done.append(currPoint)

            # we reached the end
            if currPoint == endPoint:
                break

            # get neighbors of current point
            neighbors = self.additionController.get_neighbors(currPoint)

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
                tileAndNeighbors = [n] + self.additionController.get_neighbors(n)

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

            # XXX could improve this to send less params, could likely determine neighbors filtered inside this function
            self._add_neighbors_to_heap(neighbors_filtered, openPoints, done, parent,
                                       cost, currPoint, endPoint, maxDepth)
        return self._get_path(parent, endPoint)

    # add all the neighbors that made it through filtering onto the priority queue for the next round of A*
    def _add_neighbors_to_heap(self, neighbors_filtered, openPoints, done, parent, cost, currPoint, endPoint, maxDepth):
        # look at all neighbors and add them to the heap
        for nbr in neighbors_filtered:
            if nbr not in done and self.additionController.point_in_board(nbr):
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
            path.append(p)
            p = parent[p]
        correctPath = [i for i in reversed(path)]
        return correctPath

    def _finalize_board(self):
        if len(self.rooms) == 0:
            return False
        StartRoom = self.rooms[0]

        # https://www.geeksforgeeks.org/longest-path-undirected-tree/
        # this algo finds the two farthest nodes in an undirected tree. This only works because
        # the map has no cycles (like A -> B -> C -> A)
        # XXX I'm not sure if find_farthest_room could handle cycles, I should look into that
        RoomFarthestFromStart, farthestfromStart, _ = self.autoconnect.find_farthest_room(StartRoom)
        _, farthestFromGoal, _ = self.autoconnect.find_farthest_room(RoomFarthestFromStart)
        self.additionController.setGoalSpace(farthestfromStart)
        self.additionController.setStartSpace(farthestFromGoal)
        return True

    def try_connect_board_automatically(self):
        if self.autoconnect.connect_graph(self):
            return self._finalize_board()
        return False

    def get_copy(self):
        return deepcopy(self)
    
    def get_finalized_board(self):
        return self.additionController.board # XXX don't grab their attributes like that :(









    # 3 rooms, each are their own strongly connected component
    # for a given anchor, it has 2 neighbors in this case: the closest anchor (that is not
    # invalid) from the other two rooms.  When you try to connect, you use _depth_limited_search() to see
    # if there's a path within reason that connects the two points.  If not, you invalidate those as neighbors.
    # You should be inspecting these pairs of anchors ordered by which two are the closest.
    # Each iteration you recalculate the connected components and re

    # NO TO THE ABOVE, Use Kruskal's algo.  So first, calculate the distance between each pair of anchors.  Don't use a pair that's invalidated

