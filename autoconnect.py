
from itertools import combinations
from queue import Queue, PriorityQueue

class Autoconnect(object):
    def __init__(self):
        self._edges = dict()
        self._invalidNeighbors = dict()
        self._anchors = []
        self._anchor_to_room_map = dict()


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

    # add an edge between two nodes
    def add_edge(self, p1, p2):
        self.__cross_connect(p1, p2, self._edges)

    # test if an edge exists between two nodes
    def have_edge(self, p1, p2):
        return self.__check_with_keyerror(p1, p2, self._edges)

    def invalidate(self, p1, p2):
        self.__cross_connect(p1, p2, self._invalidNeighbors)

    def points_are_invalid(self, p1, p2):
        return self.__check_with_keyerror(p1, p2, self._invalidNeighbors)

    # get all points that have an edge with this point
    # if there are none, return []
    def get_neighbors(self, point):
        return self._edges.setdefault(point, [])

    # connects all the anchors in a room to each other and tracks them.
    # formally, the anchors are nodes and we put edges between every node pair in the room
    def add_anchors(self, room):
        # connect the anchors in the edge list to make the room a strongly connected component
        anchors = room.getAnchors()
        self._anchors.extend(anchors)
        for anchor1, anchor2 in combinations(anchors, 2):
            anchor1x, anchor1y = anchor1
            anchor2x, anchor2y = anchor2
            self.add_edge(anchor1, anchor2)

        # make it O(1) to figure out which room a point is in
        for a in anchors:
            self._anchor_to_room_map[a] = room

    # return every node reachable by a given node by edges on the graph
    def get_reachable_nodes(self, givenNode):

        layers = dict()
        seen = dict()
        q = Queue()
        q.put(givenNode)

        while not q.empty():
            node = q.get()
            seen[node] = True
            for nbr in self.get_neighbors(node):
                if not seen.setdefault(nbr, False):
                    q.put(nbr)

        return list(seen.keys()), []

    def find_farthest_room(self, givenRoom):
        pass



