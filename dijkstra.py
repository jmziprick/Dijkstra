import sys
import copy

class Node:
	def __init__(self, x, y, cost, goal, start):
		self.x = x #pos X
		self.y = y #pos Y
		self.goal = goal #goal?
		self.start = start #start?
		self.cost = cost #cost of tile
		self.nodeID = "{}{}".format(str(x), str(y)) #unique node identifier

class NodeRecord:
	def __init__(self, x, y, cost, goal, start, connection, costSoFar):
		self.node = Node(x, y, cost, goal, start) #create new node for record
		self.connection = connection
		self.costSoFar = costSoFar

def pathfind(graph, startX, startY, arr):
	startRecord = NodeRecord(startX, startY, 0, False, True, None, 0)

	openList = []
	closedList = []
	openList.append(startRecord)

	while len(openList) > 0:
		current = smallestElement(openList)

		if current.node.goal == True:
			break

		connections = getConnections(current, arr) #gets adjacent nodes and stores in connections list

		#search connections for new nodes
		for connection in connections:
			endNodeCost = current.costSoFar + connection.node.cost

			if containsNode(connection.node.nodeID, closedList): #closed node, skip
				continue

			elif containsNode(connection.node.nodeID, openList): #worse route, skip
				if connection.node.cost <= endNodeCost:
					continue

			#new node record found add it to list
			connection.node.goal = goalNode(connection.node.x, connection.node.y, arr) #set goal node flag

			if containsNode(connection.node.nodeID, openList) == False:
				openList.append(connection)

		#find and remove current node from open list and add to closed list
		removeNode(current, openList)
		closedList.append(current)

	path = []
	if current.node.goal == False: #there is no possible solution
		print("No solution\n")

	else: #compile list of connections
		while current.node.start == False:
			path.append(current)
			current = current.connection
	
	return reversed(path)

def removeNode(node, openList):
	pos = 0
	for i in openList:
		if i.node.x == node.node.x and i.node.y == node.node.y:
			del openList[pos]
		pos += 1	

def containsNode(nodeID, nodeList):
	for record in nodeList:
		if record.node.nodeID == nodeID:
			return True

	return False

def getConnections(current, arr):
	connections = []
	lastCost = current.costSoFar
	x = current.node.x
	y = current.node.y

	#add any valid connecting nodes from current node
	if outOfBounds(x + 1, y, arr) == False and arr[y][x + 1] != '#':
		currCost = getCost(x + 1, y, arr)
		node = NodeRecord(x + 1, y, currCost, goalNode(x + 1, y, arr), False, current, lastCost + currCost)
		connections.append(node)

	if outOfBounds(x - 1, y, arr) == False and arr[y][x - 1] != '#':
		currCost = getCost(x - 1, y, arr)
		node = NodeRecord(x - 1, y, currCost, goalNode(x - 1, y, arr), False, current, lastCost + currCost)
		connections.append(node)

	if outOfBounds(x, y + 1, arr) == False and arr[y + 1][x] != '#':
		currCost = getCost(x, y + 1, arr)
		node = NodeRecord(x, y + 1, currCost, goalNode(x, y + 1, arr), False, current, lastCost + currCost)
		connections.append(node)

	if outOfBounds(x, y - 1, arr) == False and arr[y - 1][x] != '#':
		currCost = getCost(x, y - 1, arr)
		node = NodeRecord(x, y - 1, currCost, goalNode(x, y - 1, arr), False, current, lastCost + currCost)
		connections.append(node)

	return connections

def getCost(x, y, arr):
	if isNum(arr[y][x]):
		return int(arr[y][x])

	#no cost for goal
	elif arr[y][x] == 'G':
		return 0

	#error
	return -1

def isNum(n):
	try:
		int(n)
		return True

	except ValueError:
		return False

def goalNode(x, y, arr):
	if arr[y][x] == 'G':
		return True

	return False

def outOfBounds(x, y, arr):
	if x >= len(arr[0]):
		return True

	elif x < 0:
		return True

	if y >= len(arr):
		return True

	elif y < 0:
		return True

	return False

def smallestElement(openList):
	tmpNode = NodeRecord(None, None, None, None, None, None, None)
	smallest = 9999
	for i in openList:
		if i.node.cost < smallest:
			smallest = i.node.cost
			tmpNode = i

	return tmpNode

def getStart(arr):
	startX = 0
	startY = 0

	for j in range(0, 7):
		for i in range(0, 10):
			if arr[j][i] == 'S':
				startX = i
				startY = j

	coords = (startX, startY)
	return coords

def main():
	arr = [[]]

    #test data
	tmp = ['S', '1', '8', '1', '1', '1', '1', '1', '1', '1']
	arr[0] = tmp
	tmp = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
	arr.append(tmp)
	tmp = ['2', '1', '3', '1', '1', '1', '1', '1', '1', '1']
	arr.append(tmp)
	tmp = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '9']
	arr.append(tmp)
	tmp = ['1', '1', '1', '9', '1', '1', '1', '1', '5', '1']
	arr.append(tmp)
	tmp = ['4', '1', '9', '1', '1', '1', '1', '1', '1', '1']
	arr.append(tmp)
	tmp = ['1', '9', '1', '1', '1', '1', '1', '1', '1', 'G']
	arr.append(tmp)

	startCoord = getStart(arr)
	path = pathfind(arr, startCoord[0], startCoord[1], arr)
	for i in path:
		arr[i.node.y][i.node.x] = '@'

	for j in range(0, 7):
		for i in range(0, 10):			
			sys.stdout.write(arr[j][i])
		sys.stdout.write("\n")
	
if __name__ == "__main__":
	main()
