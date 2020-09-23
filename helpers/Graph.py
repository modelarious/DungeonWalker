from itertools import combinations
from queue import Queue
from helpers.ManhattenDistance import manhatten_distance

#Separating the data structure (Graph) from the algorithm that uses it (Autoconnect)
class Graph(object):
    def __init__(self):
        self._edges = dict()
        self._nodes = []
        self._node_to_room_map = dict()

    def get_nodes(self):
        return self._nodes
    
    # add an edge between two nodes
    # XXX What you're looking for here is a map of sets
    def _add_edge(self, p1, p2):
        if p1 not in self._edges:
            self._edges[p1] = dict()
        if p2 not in self._edges:
            self._edges[p2] = dict()

        self._edges[p1][p2] = True
        self._edges[p2][p1] = True

    # get all points that have an edge with this point
    # if there are none, return []
    def get_neighbors(self, point):
        # return self._edges[point] or []
        return self._edges.setdefault(point, [])

    # connects all the anchors in a room to each other and tracks them.
    # formally, the anchors are nodes and we put edges between every node pair in the room
    def add_room(self, room):
        # connect the anchors in the edge list to make the room a strongly connected component
        nodes = room.get_anchors()

        self._nodes.extend(nodes)
        for node1, node2 in combinations(nodes, 2):
            node1x, node1y = node1
            node2x, node2y = node2
            self._add_edge(node1, node2)

        # make it O(1) to figure out which room a point is in
        for n in nodes:
            self._node_to_room_map[n] = room
    
    # return every node reachable from a given node by following edges on the graph
    # also return how many nodes it takes to get to each one
    def _get_reachable_nodes(self, givenNode):

        layers = dict({0: [givenNode]})
        seen = [] # XXX should be a set
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

    # find farthest room from given room based on number of points you must pass through
    # NOT based on geographical location
    def find_farthest_room(self, givenRoom):
        corresponding_givenRoom_anchor = None
        farthest_point = None
        farthest_point_value = 0
        for a in givenRoom.get_anchors():
            _, layers = self._get_reachable_nodes(a)
            maxDepth = max(layers.keys())
            for node in layers[maxDepth]:
                dist = manhatten_distance(*node, *a)
                if dist > farthest_point_value:
                    farthest_point = node
                    farthest_point_value = dist
                    corresponding_givenRoom_anchor = a

        # guaranteed there will be a best pair, as the best pair will at least be two anchors in the same room
        return self._node_to_room_map[farthest_point], farthest_point, corresponding_givenRoom_anchor
