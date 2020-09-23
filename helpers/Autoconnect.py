
from itertools import combinations
from queue import Queue, PriorityQueue
from helpers.ManhattenDistance import manhatten_distance
from uuid import uuid4
from helpers.FasterPriorityQueue import FasterPriorityQueue

# This code exists to track a graph of nodes and their edges.  It is able to efficiently check
# if the current graph is connected and to connect the nodes on the graph with a minimum spanning
# tree.
# I keep track of all the connected components and update that knowledge every
# time an edge is added. This way we know when the graph is completely connected because 
# there will only be a single component on the graph (and therefore it will contain all the nodes).
# something like: 
#   [ (p1), (p2), (p3) ]
#    then p1 and p2 get connected
#   [ (p1, p2), (p3)]
#    then p3 is connected
#   [ (p1, p2, p3) ]
# you are done
#
# so the way to tackle this would be set of sets { {p1}, {p2, p3}, {p4} }
# then you can check if p2 and p3 are in the same set.
#
# but there's a way to improve on this.
# if you model the above as
# point_to_component_map = { 
#   p1 : 1,
#   p2 : 2,
#   p3 : 2,
#   p4 : 3
# }
# then you can just check if the graph component number is the same and you have
# O(1) access to this check

# also going in reverse so that we can find all nodes that belong to a component when we connect two components
# component_to_point_map = {
#    1 : { p1 },
#    2 : { p2, p3 },
#    3 : { p4 }
# }

# then when you connect two components, you just have to add their sets together and change the component number.
# using the above data to start, this example is the state after connecting up p2 to p1:
# { 
#   p1 : 1,
#   p2 : 1,
#   p3 : 1,
#   p4 : 3
# }
# {
#    1 : { p1 , p2, p3},
#    3 : { p4 }
# }

# - to calculate if all nodes are reachable, check that there is only one key in component_to_point_map
# - to check if the rooms already have a path to each other, check if their component number is the same
# - initialize to : no points on graph
# - when add_room is used: each room is added as a component, and all 4 points in the room are added
class Autoconnect(object):
    def __init__(self):
        self._edges = dict()
        self._anchors = []
        self._anchor_to_room_map = dict()
        self._point_to_component_map = dict()
        self._component_to_point_map = dict()


    # XXX what do we use this for??
    def __cross_connect(self, p1, p2, d):
        # partner function with __check_with_keyerror, we store True at d[p1][p2] so that we can check
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

    # test if an edge exists between two nodes
    def have_edge(self, p1, p2):
        # XXX WE CAN CALCULATE THIS DIFFERENTLY!!!
        # XXX points_already_have_path
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

        # XXX what do we use this for?? it's a collection of all nodes, but do we need this?
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

    # def _compute_all_unused_possible_edges_slow(self):
    #     q = PriorityQueue()
    #     for a1 in self._anchors:
    #         for a2 in self._anchors:
    #             if self.points_already_have_path(a1, a2):
    #                 continue
                
    #             # something like ( 5 , ((1, 1), (6, 1)) )
    #             distance_edge_tuple = (
    #                 manhatten_distance(*a1, *a2),
    #                 (a1, a2)
    #             )
    #             q.put(distance_edge_tuple)
    #     print("finished generating queue")
    #     return q
    
    # fastest of the 3 methods, but less intuitive than using FasterPriorityQueue
    # def _compute_all_unused_possible_edges_dict(self):
    #     d = dict()
    #     for a1 in self._anchors:
    #         for a2 in self._anchors:
    #             currEdge = (a1, a2)
    #             if self.points_already_have_path(*currEdge):
    #                 continue
            
    #             distanceKey = manhatten_distance(*a1, *a2)
    #             if distanceKey not in d:
    #                 d[distanceKey] = set()
    #             d[distanceKey].add(currEdge)
    #     print("finished generating queue")
    #     return d
    
    def _compute_all_unused_possible_edges(self):
        return FasterPriorityQueue(self._anchors, self)

    def connect_graph(self, mapGenerationEngine):
        # returns a priority queue where we consider smallest edges first
        consideredEdges = self._compute_all_unused_possible_edges()

        # XXX in the case of two rooms, you will never get to check if the graph is already connected
        while not consideredEdges.empty():
            edge = consideredEdges.get()

            # first, if all nodes in the graph are reachable, then we've finished
            if self._graph_is_connected():
                return True
            
            # if there already exists a path between these two points, then continue
            if self.points_already_have_path(*edge):
                continue

            # if we succeeded in connecting the two nodes, then update connected components
            if mapGenerationEngine.connect_path_nodes(*edge):
                self._connect_components(*edge)
                self._add_edge(*edge)

        # if the graph is now connected, then return true.
        if self._graph_is_connected():
            return True
        
        return False

    def _graph_is_connected(self):
        components = self._component_to_point_map.keys()
        return len(components) == 1

    def _get_components(self, fromPoint, toPoint):
        fromComponent = self._point_to_component_map[fromPoint]
        toComponent = self._point_to_component_map[toPoint]
        return fromComponent, toComponent
    
    def points_already_have_path(self, fromPoint, toPoint):
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
        
        

