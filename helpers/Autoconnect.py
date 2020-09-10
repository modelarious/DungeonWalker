
from itertools import combinations
from queue import Queue, PriorityQueue
from helpers.ManhattenDistance import manhatten_distance
from uuid import uuid4

class Autoconnect(object):
    def __init__(self):
        self._edges = dict()
        self._anchors = []
        self._anchor_to_room_map = dict()

        # The best way to do this would have a map -> set number.
        # so the way to tackle this would be set of sets { {p1}, {p2, p3}, {p4}}
        # then you can check if p2 and p3 are in the same set.
        #
        # but there's a way to improve on this
        # if you model the above as
        # self._point_to_component_map = { 
        #   p1 : 1,
        #   p2 : 2,
        #   p3 : 2,
        #   p4 : 3
        # }
        # then you can just check if the set number is the same and you have
        # O(1) access to the values

        # also going to need the reverse:
        # self._component_to_point_map = {
        #    1 : { p1 },
        #    2 : { p2, p3 },
        #    3 : { p4 }
        # }
        # so that we can find all nodes that belong to a set when we connect two sets
        self._point_to_component_map = dict()
        self._component_to_point_map = dict()

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
    def _add_edge(self, p1, p2):
        self.__cross_connect(p1, p2, self._edges)
        # from pprint import pprint
        # print(f"cross connected the edge {p1}, {p2}, now edges is")
        # pprint(self._edges)

    # test if an edge exists between two nodes
    def have_edge(self, p1, p2):
        return self.__check_with_keyerror(p1, p2, self._edges)

    # get all points that have an edge with this point
    # if there are none, return []
    def get_neighbors(self, point):
        # return self._edges[point] or []
        return self._edges.setdefault(point, [])
    
    def add_room(self, room):
        self._add_nodes(room)
        componentID = str(uuid4())
        component = set()
        for node in room.get_anchors():
            component.add(node)
            self._point_to_component_map[node] = componentID
        
        self._component_to_point_map[componentID] = component

    # connects all the anchors in a room to each other and tracks them.
    # formally, the anchors are nodes and we put edges between every node pair in the room
    def _add_nodes(self, room):
        # connect the anchors in the edge list to make the room a strongly connected component
        anchors = room.get_anchors()
        self._anchors.extend(anchors)
        for anchor1, anchor2 in combinations(anchors, 2):
            anchor1x, anchor1y = anchor1
            anchor2x, anchor2y = anchor2
            self._add_edge(anchor1, anchor2)

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
        for a in givenRoom.get_anchors():
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

    def _compute_all_unused_possible_edges(self):
        q = PriorityQueue()
        for a1 in self._anchors:
            for a2 in self._anchors:
                if a1 == a2:
                    continue

                if self.have_edge(a1, a2):
                    continue
                
                # something like ( 5 , ((1, 1), (6, 1)) )
                distance_edge_tuple = (
                    manhatten_distance(*a1, *a2),
                    (a1, a2)
                )
                q.put(distance_edge_tuple)
        return q

    def connect_graph(self, mapGenerationEngine):
        # from pprint import pprint
        # print("connect_graph was called")
        # pprint("self.edges: ")
        # pprint(self._edges)
        # pprint(f"self._anchors {self._anchors}")
        # pprint(f"self._anchor_to_room_map {self._anchor_to_room_map}")

        # returns a priority queue where we consider smallest edges first
        consideredEdges = self._compute_all_unused_possible_edges()

        while not consideredEdges.empty():
            dist, edge = consideredEdges.get()

            # print(f"DIST='{dist}' edge='{edge}'")

            # # if we don't want to connect these two points for any reason
            # XXX in the case of two rooms, you will never get to check if the graph is already connected
            # you need to refine your approach here. get_reachable_nodes is returning a list that contains the same values multiple times,
            # there has got to be a better way to traverse this graph, or at least keep track of which rooms
            # are already connected instead of doing it by point, so that the get_reachable_nodes call
            # isn't so expensive.  If you keep track of all the connected components and update that knowledge every
            # time an edge is added, you will know when the graph is completely connected because there will only
            # be a single component on the graph (and therefore it will contain all the nodes).
            # something like: 
            #   [ (r1), (r2), (r3) ]
            #    then r1 and r2 get connected
            #   [ (r1, r2), (r3)]
            #    then r3 is connected
            #   [ (r1, r2, r3) ]
            # you are done

            # The best way to do this would have a map -> set number.
            # so the way to tackle this would be set of sets { {p1}, {p2, p3}, {p4}}
            # then you can check if p2 and p3 are in the same set.
            #
            # but there's a way to improve on this
            # if you model the above as
            # { 
            #   p1 : 1,
            #   p2 : 2,
            #   p3 : 2,
            #   p4 : 3
            # }
            # then you can just check if the set number is the same and you have
            # O(1) access to the values

            # also going to need the reverse:
            # {
            #    1 : { p1 },
            #    2 : { p2, p3 },
            #    3 : { p4 }
            # }
            # so that we can find all nodes that belong to a set when we connect two sets

            # to calculate if all nodes are reachable, check that there is only one key in the reverse

            # to check if the rooms already have a path to each other, check if their set number is the same

            # initialize to : each room is its own set of points

            # anyways....

            # first, if all nodes in the graph are reachable, then we've finished
            if self._graph_is_connected():
                return True
            
            # if there already exists a path between these two points, then continue
            if self._points_already_have_path(*edge):
                continue

            # if we succeeded in connecting the two nodes, then update connected components
            if mapGenerationEngine.connect_path_nodes(*edge):
                self._connect_components(*edge)
                self._add_edge(*edge)

        return False

    def _graph_is_connected(self):
        components = self._component_to_point_map.keys()
        return len(components) == 1

    def _get_components(self, fromPoint, toPoint):
        fromComponent = self._point_to_component_map[fromPoint]
        toComponent = self._point_to_component_map[toPoint]
        return fromComponent, toComponent
    
    def _points_already_have_path(self, fromPoint, toPoint):
        fromComponent, toComponent = self._get_components(fromPoint, toPoint)
        return fromComponent == toComponent

    def _connect_components(self, fromPoint, toPoint):
        fromComponent, toComponent = self._get_components(fromPoint, toPoint)

        # move all elements from the "fromComponent" to the "toComponent"
        for pt in self._component_to_point_map[fromComponent]:
            self._point_to_component_map[pt] = toComponent

        toSet = self._component_to_point_map[toComponent]
        fromSet = self._component_to_point_map[fromComponent]

        # add all points to the toComponent and remove the fromComponent
        self._component_to_point_map[toComponent] = toSet.union(fromSet)
        del self._component_to_point_map[fromComponent]
        
        

