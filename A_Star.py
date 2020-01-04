from heapq import heappush, heappop

'''
#from https://webdocs.cs.ualberta.ca/~hayward/355/jem/tile.html
#fetched December 25, 2019

fringe = PQ()
fringe.add(start, 0)
parent, cost, done = {}, {}, []
parent[start], cost[start] = None, 0
#cost[v] will be min dist-so-far from start to v
#if heuristic(target, v) is always less/equal than min dist(target,v),
#then final cost[v] will be min dist from start to v

while not fringe.empty():
  current = fringe.remove() # min priority
  done.add(current)
  if current == target: break
  for next in nbrs(current):
    if next not in done:
      new_cost = cost[current] + wt(current, next)
        if next not in cost or new_cost < cost[next]:
          cost[next] = new_cost
          priority = new_cost + heuristic(target, next)
          fringe.add(next, priority)
          parent[next] = current
'''


'''
defines the a star algorithm from "startNode" to "endNode", where heuristic is 
a function that returns the heuristic value between two nodes (ie:
heuristic(currNode, endNode) returns the heuristic between the current node and the end
'''
def a_star(startNode, endNode, heuristic, neighborDict):

	#first element in open list is the start node
	openNodes = []
	heappush(openNodes, (0, startNode))

	parent, cost, done = {}, {}, []
	parent[startNode] = None
	cost[startNode] = 0

	while len(openNodes) != 0:
		prio, currNode = heappop(openNodes)
		done.append(currNode)
		if currNode == endNode: break

		for nbr in neighborDict[currNode]:
			if nbr not in done:
				updatedCost = cost[currNode] + neighborDict[currNode][nbr]
				if nbr not in cost or updatedCost < cost[nbr]:
					cost[nbr] = updatedCost
					priority = updatedCost + heuristic(nbr, endNode)
					heappush(openNodes, (priority, nbr))
					parent[nbr] = currNode

	#follow the path backwards and print it
	path = []
	p = parent[endNode]
	path.append(endNode)
	while p != None:
		path.append(p)
		p = parent[p]
	correctPath = [i for i in reversed(path)]
	print(correctPath)
	return correctPath

nD = {
        "Oradea" : {
                "Zerind": 75,
                "Siblu": 151
        },      
        "Zerind" : {
                "Oradea" : 71,
		"Arad" : 75
        },
        "Arad" : {
                "Siblu": 140,
		"Zerind": 75,
		"Timinisoara" : 118
        },
	"Timinisoara" : {
		"Arad" : 118,
		"Lugoj" : 70
	},
	"Siblu" : {
		"Oradea" : 151,
		"Arad" : 140,
		"Fagaras" : 99,
		"Rimnicu" : 80
	},
	"Lugoj" : {
		"Timinisoara" : 70,
		"Pitesti" : 403
	},
	"Rimnicu" : {
		"Pitesti": 97,
		"Siblu" : 80
	},
	"Fagaras" : {
		"Siblu" : 99,
		"Bucharest" : 211
	},
	"Pitesti" : {
		"Rimnicu" : 97,
		"Lugoj" : 403,
		"Bucharest" : 101
	}		
}

def myHeuristic(a, b):
	if a == "Arad": return 366
	if a == "Bucharest": return 0
	if a == "Oradea": return 380
	if a == "Zerind": return 374
	if a == "Timinisoara": return 329
	if a == "Siblu": return 253
	if a == "Lugoj": return 244
	if a == "Rimnicu": return 193
	if a == "Fagaras": return 176
	if a == "Pitesti": return 10
	else: return 100000

a_star("Oradea", "Bucharest", myHeuristic, nD)


