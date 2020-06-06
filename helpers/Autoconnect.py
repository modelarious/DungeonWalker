
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

    def _invalidate(self, p1, p2):
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

    # return every node reachable from a given node by following edges on the graph
    # also return how many nodes it takes to get to each one
    def get_reachable_nodes(self, givenNode):

        layers = dict({0: [givenNode]})
        seen = []
        q = Queue()

        # (depth, node)
        q.put((0, givenNode))

        while not q.empty():
            depth, node = q.get()
            seen.append(node)

            nbr_layer = []
            nbr_layer_number = depth + 1

            for nbr in self.get_neighbors(node):
                if nbr not in seen:
                    q.put((nbr_layer_number, nbr))
                    seen.append(nbr)

                    nbr_layer.append(nbr)

            if nbr_layer:
                if nbr_layer_number not in layers:
                    layers[nbr_layer_number] = []
                layers[nbr_layer_number].extend(nbr_layer)

        return seen, layers

    # find farthest room from given room based on number of anchors you must pass through
    # NOT based on geographical location
    def find_farthest_room(self, givenRoom):
        corresponding_givenRoom_anchor = None
        farthest_point = None
        farthest_point_value = 0
        for a in givenRoom.getAnchors():
            _, layers = self.get_reachable_nodes(a)
            maxDepth = max(layers.keys())
            for node in layers[maxDepth]:
                dist = manhatten_distance(*node, *a)
                if dist > farthest_point_value:
                    farthest_point = node
                    farthest_point_value = dist
                    corresponding_givenRoom_anchor = a

        # guaranteed there will be a best pair, as the best pair will at least be two anchors in the same room
        return self._anchor_to_room_map[farthest_point], farthest_point, corresponding_givenRoom_anchor

    # give it the two points that were just successfully connected,
    # don't consider any more connections between these rooms
    def _invalidate_rooms(self, p1, p2):
        r1, r2 = self._anchor_to_room_map[p1], self._anchor_to_room_map[p2]
        for a1 in r1.getAnchors():
            for a2 in r2.getAnchors():
                self._invalidate(a1, a2)

    def _compute_all_unused_possible_edges(self):
        q = PriorityQueue()
        for a1 in self._anchors:
            for a2 in self._anchors:
                if self.have_edge(a1, a2):
                    continue
                # something like ( 5 , ((1, 1), (6, 1)) )
                distance_edge_tuple = (
                    manhatten_distance(*a1, *a2),
                    (a1, a2)
                )
                q.put(distance_edge_tuple)
        return q

    def connect_graph(self, board):
        # returns a priority queue where we consider smallest edges first
        consideredEdges = self._compute_all_unused_possible_edges()
        while not consideredEdges.empty():
            dist, edge = consideredEdges.get()

            # if we don't want to connect these two points for any reason
            if self.points_are_invalid(*edge):
                continue

            # if the graph is already connected, can stop
            reachable, _ = self.get_reachable_nodes(edge[0])
            if set(reachable) == set(self._anchors):
                return True

            # don't connect two rooms if they already have a path to each other
            if edge[1] in reachable:
                continue

            # if we can connect the two nodes, then do it and
            # don't consider anymore connections between these two rooms
            if board.connect_path_nodes(*edge):
                self._invalidate_rooms(*edge)

        return False




def manhatten_distance(p1X, p1Y, p2X, p2Y):
    return abs(p1X - p2X) + abs(p1Y - p2Y)