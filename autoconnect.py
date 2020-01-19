
from itertools import combinations

class Autoconnect(object):
    def __init__(self):
        self._edges = dict()
        self._invalidNeighbors = dict()
        self._anchors = [] #XXX TODO need this feature to be able to iterate through all anchors


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
    def add_edge(self, p1, p2):
        self.__cross_connect(p1, p2, self._edges)

    def have_edge(self, p1, p2):
        return self.__check_with_keyerror(p1, p2, self._edges)

    def invalidate(self, p1, p2):
        self.__cross_connect(p1, p2, self._invalidNeighbors)

    def points_are_invalid(self, p1, p2):
        return self.__check_with_keyerror(p1, p2, self._invalidNeighbors)

    # going to be used for autoconnect feature, so not tested yet
    def get_neighbors(self, point):
        try:
            return self._edges[point]
        except KeyError:
            return False

    def add_anchors(self, room):
        # connect the anchors in the edge list to make the room a strongly connected component
        anchors = room.getAnchors()
        self._anchors.extend(anchors)
        for anchor1, anchor2 in combinations(anchors, 2):
            anchor1x, anchor1y = anchor1
            anchor2x, anchor2y = anchor2
            self.add_edge(anchor1, anchor2)