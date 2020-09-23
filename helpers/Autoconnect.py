from helpers.FasterPriorityQueue import FasterPriorityQueue
from helpers.Graph import Graph
from uuid import uuid4

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
# so one way to tackle this would be list of sets [ {p1}, {p2, p3}, {p4} ]
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
# then you can just check if the graph component number is the same for p2 and p3 and you have
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
        self._point_to_component_map = dict()
        self._component_to_point_map = dict()
        self._graph = Graph()

    def points_already_have_path(self, fromPoint, toPoint):
        fromComponent, toComponent = self._get_components(fromPoint, toPoint)
        return fromComponent == toComponent

    def add_room(self, room):
        self._graph.add_room(room)
        componentID = str(uuid4())
        component = set()
        for node in room.get_anchors():
            component.add(node)
            self._point_to_component_map[node] = componentID
        
        self._component_to_point_map[componentID] = component
    
    def find_farthest_room(self, givenRoom):
        return self._graph.find_farthest_room(givenRoom)

    def connect_graph(self, mapGenerationEngine):
        # returns a priority queue where we consider shortest edge candidates first
        consideredEdges = self._compute_all_unused_possible_edges()

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
                self._graph._add_edge(*edge)

        # if the graph is now connected, then we succeeded
        if self._graph_is_connected():
            return True
        
        return False

    def _compute_all_unused_possible_edges(self):
        return FasterPriorityQueue(self._graph.get_nodes(), self)

    def _graph_is_connected(self):
        components = self._component_to_point_map.keys()
        return len(components) == 1

    def _get_components(self, fromPoint, toPoint):
        fromComponent = self._point_to_component_map[fromPoint]
        toComponent = self._point_to_component_map[toPoint]
        return fromComponent, toComponent

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