from helpers.ManhattenDistance import manhatten_distance
class FasterPriorityQueue(object):

    def __init__(self, nodeList, autoconnect):
        self.edgeDict = dict()
        self._populate_edge_dict(nodeList, autoconnect)

    def _populate_edge_dict(self, nodes, autoconnect):
        for p1 in nodes:
            for p2 in nodes:
                currEdge = (p1, p2)
                if p1 == p2 or autoconnect.points_already_have_path(*currEdge):
                    continue

                distanceKey = manhatten_distance(*p1, *p2)
                self.put(currEdge, distanceKey)

        print("finished generating queue")
    
    def put(self, val, prio):
        if prio not in self.edgeDict:
            self.edgeDict[prio] = set()
        self.edgeDict[prio].add(val)

    def get(self):
        minPrio = min(self.edgeDict.keys())
        returnVal = self.edgeDict[minPrio].pop()
        if self.edgeDict[minPrio] == set():
            del self.edgeDict[minPrio]
        return returnVal
    
    def empty(self):
        return self.edgeDict == dict()