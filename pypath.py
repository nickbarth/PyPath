#!/usr/bin/env python

# PyPath
# Nick Barth 2010

from Tkinter import *

def main():
	global myArea,     \
		   dataList,   \
		   openList,   \
		   closedList, \
		   startPoint, \
		   endPoint,   \
		   path,       \
		   currentNode \
	
	# Path Finding Map
	myArea = [[2,0,0,0,0,0,0,0,1,0],
			  [1,1,1,0,0,0,0,1,1,0],
			  [0,0,1,1,0,1,1,1,0,0],
			  [0,0,1,0,0,1,0,0,0,0],
			  [1,0,0,0,1,1,0,1,1,0],
			  [0,1,1,1,1,0,1,1,0,0],
			  [0,0,1,0,0,1,1,0,0,0],
			  [0,1,1,0,1,1,0,0,0,0],
			  [0,1,0,1,1,0,1,0,0,0],
			  [0,0,1,1,0,0,1,0,0,3]]
	
	# Location in [Y, X] format
	# Find start and End Point
	for y in range(len(myArea)):
		for x in range(len(myArea[0])):
			if myArea[y][x] == 2:
				startPoint = [y,x]
			if myArea[y][x] == 3:
				endPoint = [y,x]
	
	# Initialize dataList with start point
	dataList = [[False for x in range(len(myArea[0]))] for x in range(len(myArea))]
	dataList[startPoint[0]][startPoint[1]] = {
					"parent" : False,
					"gScore" : 0,
					"hScore" : 0,
					"fScore" : 0
				 }
	openList = []
	closedList = []
	
	currentNode = startPoint
	pathFound = False
	
	# A* Method Begins
	# Add the starting node to the open list
	openList.append(currentNode)
	
	
	# Repeat the following
	# until you  a) Fail to find the target node and the open list is empty meaning there is no path
	#        or  b) Add the target node to the closed list meaning the path has been found
	while openList and not pathFound:
		# Look for the lowest F cost node on the open list
		# Refer to this as the current node
		openList.sort(sortOpenList)
		currentNode = openList.pop(0)
		
		# Switch it to the closed list
		closedList.append(currentNode)
		
		if (currentNode == endPoint):
			pathFound = True
		else:
			# Get each of the 8 node adjacent to this current node
			getAdjacentNodes()
	
	# Save the Path 
	if pathFound:
		path = []
		retraceNode = endPoint
		# Retrace the path backwards from the target node
		# Get each parent node until you reach the starting node
		while retraceNode:
			path.append(retraceNode)
			retraceNode = dataList[retraceNode[0]][retraceNode[1]]["parent"]
		# Draw Path
		drawPath()
	else:
		print "No Path Found."
	

def isValidNode(node):
	# X and Y in Bounds and Not Invalid
	if node[1] > -1 and \
	   node[1] < len(myArea[0]) and \
	   node[0] > -1 and \
	   node[0] < len(myArea) and \
	   myArea[node[0]][node[1]] != 1 and \
	   not node in closedList:
		return True
	return False

def getAdjacentNodes():
	for yCheck in range(-1,2):
		for xCheck in range(-1,2):
			yPos = currentNode[0] + yCheck
			xPos = currentNode[1] + xCheck
			
			# Ignore the node if it on the closed list or not walkable
			if [yPos,xPos] != currentNode and isValidNode([yPos,xPos]):
				# If the node isnt on the open list add it and record the F, G, and H scores 
				if not [yPos,xPos] in openList:
					openList.append([yPos,xPos])
					addToDataList([yPos,xPos])

				# If its on the open list check to see if this path is better
				# Lower G scores means its a better path
				else:
					# Update parent node and recalculate its G and F scores
					if dataList[yPos][xPos]["gScore"] > determineGScore([yPos,xPos], currentNode):
						addToDataList([yPos,xPos])
	return

def determineGScore(node, parent):
	parentGScore = dataList[parent[0]][parent[1]]["gScore"]
	if node[0] == currentNode[0] or node[1] == currentNode[1]:
		return 10 + parentGScore
	return 14 + parentGScore

def determineHScore(node):
	return (abs(node[0] - endPoint[0]) + abs(node[1] - endPoint[1])) * 10

def determineFScore(gScore, hScore):
	return gScore + hScore

def getFoundNode(node):
	search = filter(lambda checkNode: checkNode["yPos"] == node[0] and checkNode["xPos"] == node[1], dataList)
	return search[0] if search else False

def addToDataList(node):
	# Make the current node the parent of this node
	parent = currentNode
	gScore = determineGScore(node, parent)
	hScore = determineHScore(node)
	fScore = determineFScore(gScore, hScore)
	
	dataList[node[0]][node[1]] = {
									"parent" : parent,
									"gScore" : gScore,
									"hScore" : hScore,
									"fScore" : fScore,
									"closed" : False
								 }

def sortOpenList(x, y):
	return cmp(dataList[x[0]][x[1]]['fScore'], dataList[y[0]][y[1]]['fScore'])

def drawPath():
	root = Tk()
	root.title("A* Pathfinding by Nick Barth")
	w = Canvas(root, width=510, height=510, background="white")
	w.pack()
	for y in range(len(myArea)):
		for x in range(len(myArea[0])):
			if myArea[y][x] == 1:
				# Wall Node
				myFill = "orange"
			elif myArea[y][x] == 2:
				# Start Node
				myFill = "lightgreen"
			elif myArea[y][x] == 3:
				# End Node
				myFill = "pink"
			else:
				# Path Node
				myFill = "lightblue"
			
			w.create_rectangle(5+(50*x), 5+(50*y), 55+(50*x), 55+(50*y), fill=myFill)
			w.create_text(15+(50*x),16+(50*y), text=" "+str(y)+", "+str(x))
			
			if dataList[y][x]:
				# Node in Open List
				data = dataList[y][x]
				midColor = "blue"
		
				if [y,x] in path:
					# Node in Path
					midColor="green"
				elif [y,x] in closedList:
					# Node in Closed List
					midColor = "red"

				w.create_oval(5+(50*x)+20, 5+(50*y)+20, 55+(50*x)-20, 55+(50*y)-20, fill=midColor, outline=midColor)
				w.create_text(43+(50*x),16+(50*y), text=data["fScore"], justify="right")
				w.create_text(15+(50*x),48+(50*y), text=data["gScore"])
				w.create_text(43+(50*x),48+(50*y), text=data["hScore"], justify="right")	
	mainloop()

if __name__ == "__main__":
    main()
