##
# Here is where I pre-wrote code for use in other files. I left them here just in case of disaster.
##

fontObj = pygame.font.Font('freesansbold.ttf' , 32)
self.msg =  str(self.score)
msgSurface = fontObj.render(msg, False, red)
msgRect = msgSurface.get_rect()
msgRect.topleft = (10, 20)
def checkBugEat(self):
		#destroys blocks under bugs that have survived long enough to eat.
		exit = False
		for bug in self.bugList:
			if bug.eatRect != None:
				for row in self.playfield.cellRows:
					for col in self.playfield.cellCols:
						if isinstance(self.playfield.rectList[row][col], pg.Rect):
							if self.playfield.rectList[row][col].collidepoint(bug.eatRect.center):
								bug.eatRect = None
								self.playfield.rectList[row][col] = None
								exit = True #allows an ugly double break 
								#b/c bugs can only eat one block
								break #first for loop break
					if exit:
						break #exits second for loop in an ungraceful
						# manner to continue checking for hungry bugs!

	

def checkBugFloorsAndWalls(self):
		for bug in self.bugList:
			collisionRect = bug.rect.copy()
			#set collisionRects
			downRect = collisionRect.move(0,1)
			leftRect = collisionRect.move(-1, 0)
			rightRect = collisionRect.move(1, 0)
			changeStatus = True
			changeWallLeftStatus = False
			changeWallRightStatus = False
			for row in xrange(self.playfield.cellRows):
					for col in xrange(self.playfield.cellCols):
						#checks that the "floor" cell in question exists
						if (isinstance(self.playfield.rectList[row][col], pg.Rect)):
							if not(self.avatar.airborne):
								if self.playfield.rectList[row][col].colliderect(downRect):
									changeStatus = False
							if not(self.avatar.wallLeft):
								if self.playfield.rectList[row][col].colliderect(leftRect):
									changeWallLeftStatus = True
							if not(self.avatar.wallRight):
								if self.playfield.rectList[row][col].colliderect(rightRect):
									changeWallRightStatus = True
			bug.airborne = changeStatus
			bug.wallLeft = changeWallLeftStatus
			bug.wallRight = changeWallRightStatus

	def checkBugCollision(self):
		for bug in self.bugList:
			collisionRect = bug.rect.move(bug.xvel, bug.yvel)
			correction = False
			collisionList = []
			for row in xrange(self.playfield.cellRows):
				for col in xrange(self.playfield.cellCols):
					if (isinstance(self.playfield.rectList[row][col], pg.Rect)):
						if collisionRect.colliderect(self.playfield.rectList[row][col]):
							correction = True
							collisionList.append(self.playfield.rectList[row][col])
							self.flagBugCollisionPoints(bug, collisionRect, self.playfield.rectList[row][col])
			if correction:
				self.correctBug(bug, collisionRect, collisionList)
			else:
				if not(self.checkBugLedge(bug)):
					bug.move()
				else:
					bug.xvel = -bug.xvel
					bug.move()

	def checkBugLedge(self, bug):
		ledge = True
		testrect = bug.rect.move(bug.xvel, bug.yvel+1)
		for row in xrange(self.playfield.cellRows):
				for col in xrange(self.playfield.cellCols):
					if (isinstance(self.playfield.rectList[row][col], pg.Rect)):
						if testrect.colliderect(self.playfield.rectList[row][col]):
							ledge = False
		return ledge

	def flagBugCollisionPoints(self,bug, collisionBug, obstacle):
		if(obstacle.collidepoint(collisionBug.topright)):
			bug.flagTopRight = True
		if(obstacle.collidepoint(collisionBug.topleft)):
			bug.flagTopLeft = True
		if(obstacle.collidepoint(collisionBug.bottomright)):
			bug.flagBottomRight = True
		if(obstacle.collidepoint(collisionBug.bottomleft)):
			bug.flagBottomLeft = True

	def correctBug(self, bug, collisionRect, collisionList):
		while(bug.flagBottomLeft and bug.flagTopLeft):
			collisionRect.move_ip(2, 0)
			for obstacle in collisionList:
				if not(obstacle.collidepoint(collisionRect.topleft)):
					bug.flagTopLeft = False
				if not(obstacle.collidepoint(collisionRect.bottomleft)):
					bug.flagBottomLeft = False
			bug.xvel = 0
	#both bottom points flagged
		while(bug.flagBottomLeft and bug.flagBottomRight):
			collisionRect.move_ip(0, -1)
			for obstacle in collisionList:
				if not(obstacle.collidepoint(collisionRect.bottomleft)):
					bug.flagBottomLeft = False
				if not(obstacle.collidepoint(collisionRect.bottomright)):
					bug.flagBottomRight = False
	#both right points flagged
		while(bug.flagBottomRight and bug.flagTopRight):
			collisionRect.move_ip(-2, 0)
			for obstacle in collisionList:
				if not(obstacle.collidepoint(collisionRect.bottomright)):
					bug.flagBottomRight = False
				if not(obstacle.collidepoint(collisionRect.topright)):
					bug.flagTopRight = False
			bug.xvel = 0
	#both upper points flagged
		while(bug.flagTopRight and bug.flagTopLeft):
			collisionRect.move_ip(0,1)
			for obstacle in collisionList:
				if not(obstacle.collidepoint(collisionRect.topright)):
					flagTopRight = False
				if not(obstacle.collidepoint(collisionRect.topleft)):
					flagTopLeft = False
	#singles
		while(bug.flagTopLeft):
			collisionRect.move_ip(1, 1)
			for obstacle in collisionList:
				if not(obstacle.collidepoint(collisionRect.topleft)):
					bug.flagTopLeft = False
		while(bug.flagBottomLeft):
			collisionRect.move_ip(1, -1)
			for obstacle in collisionList:
				if not(obstacle.collidepoint(collisionRect.bottomleft)):
					bug.flagBottomLeft = False
		while(bug.flagBottomRight):
			collisionRect.move_ip(-1, -1)
			for obstacle in collisionList:
				if not(obstacle.collidepoint(collisionRect.bottomright)):
					bug.flagBottomRight
		while(bug.flagTopRight):
			collisionRect.move_ip(-1,1)
			for obstacle in collisionList:
				if not(obstacle.collidepoint(collisionRect.topright)):
					bug.flagTopRight = False
		#correct Avatar Move to coords of the collision rect
		bug.rect = collisionRect

def checkBugEatCollisions(self):
	testRect = self.bug.eatRect
	offset = 300 #screen pixels before grid in both x and y direction
	numCells = 20 #number of cells in a row/col of platform grid
	#un-converted values into list
	topleft = testRect.topleft
	topright = testRect.topright
	bottomleft = testRect.bottomleft
	bottomright = testRect.bottomright
	collisionPoints = [topleft, topright, bottomleft, bottomright]
	modelPoints = []
	collision = False
	collideRects = []
	#mathematical conversion to grid model-workable values
	for point in collisionPoints:
		(x,y) = point
		#grid-workable points are either negative (non-colliding)
		#positive and within 0-19 (numCells),
		#or 20+ (non-colliding on the right side)
		x = (x - offset)/numCells 
		y = (y - offset)/numCells
		modelPoint = (x,y)
		modelPoints.append(modelPoint)
	#evaluate collisions with only relevant grid rects
	for index, point in enumerate(modelPoints):
		#check if the bounds of the point warrant checking collision
		(x,y) = point #based on grid values...
		if (not((x < 0) or (x >= numCells)) and not((y < 0) or (y >= numCells))):
			#check collision
			if self.playfield.rectList[y][x]:
				if self.playfield.rectList[y][x].collidepoint(collisionPoints[index]): #uses actual point
					self.playfield.rectList[x][y] = None

def checkRight(self, thing): #i wrote this
	testRect = thing.rect.move(1,0)
	offset = 300 #screen pixels before grid in both x and y direction
	numCells = 20 #number of cells in a row/col of platform grid
	#un-converted values into list
	bottomleft = testRect.topright
	bottomright = testRect.bottomright
	collisionPoints = [topright, bottomright]
	modelPoints = []
	collision = False
	collideRects = []
	#mathematical conversion to grid model-workable values
	for point in collisionPoints:
		(x,y) = point
		#grid-workable points are either negative (non-colliding)
		#positive and within 0-19 (numCells),
		#or 20+ (non-colliding on the right side)
		x = (x - offset)/numCells 
		y = (y - offset)/numCells
		modelPoint = (x,y)
		modelPoints.append(modelPoint)
	#evaluate collisions with only relevant grid rects
	for index, point in enumerate(modelPoints):
		#check if the bounds of the point warrant checking collision
		(x,y) = point #based on grid values...
		if (not((x < 0) or (x >= numCells)) and not((y < 0) or (y >= numCells))):
			#check collision
			if self.playfield.rectList[y][x]:
				if self.playfield.rectList[y][x].collidepoint(collisionPoints[index]): #uses actual point
					collision = True
				#set flag
	if (collision):
		thing.wallRight = True
	else:
		thing.wallRight = False

def checkLeft(self, thing): #i wrote this
	testRect = thing.rect.move(-1,0)
	offset = 300 #screen pixels before grid in both x and y direction
	numCells = 20 #number of cells in a row/col of platform grid
	#un-converted values into list
	bottomleft = testRect.topleft
	bottomright = testRect.bottomleft
	collisionPoints = [topleft, bottomleft]
	modelPoints = []
	collision = False
	collideRects = []
	#mathematical conversion to grid model-workable values
	for point in collisionPoints:
		(x,y) = point
		#grid-workable points are either negative (non-colliding)
		#positive and within 0-19 (numCells),
		#or 20+ (non-colliding on the right side)
		x = (x - offset)/numCells 
		y = (y - offset)/numCells
		modelPoint = (x,y)
		modelPoints.append(modelPoint)
	#evaluate collisions with only relevant grid rects
	for index, point in enumerate(modelPoints):
		#check if the bounds of the point warrant checking collision
		(x,y) = point #based on grid values...
		if (not((x < 0) or (x >= numCells)) and not((y < 0) or (y >= numCells))):
			#check collision
			if self.playfield.rectList[y][x]:
				if self.playfield.rectList[y][x].collidepoint(collisionPoints[index]): #uses actual point
					collision = True
				#set flag
	if (collision):
		thing.wallLeft = True
	else:
		thing.wallLeft = False

def checkWalls(self, thing):
	self.checkLeft(self, thing)
	self.checkRight(self, thing)

def checkFloor(self, thing): #i wrote this
	testRect = thing.rect.move(0, 1)
	offset = 300 #screen pixels before grid in both x and y direction
	numCells = 20 #number of cells in a row/col of platform grid
	#un-converted values into list
	bottomleft = testRect.bottomleft
	bottomright = testRect.bottomright
	collisionPoints = [bottomleft, bottomright]
	modelPoints = []
	collision = False
	collideRects = []
	#mathematical conversion to grid model-workable values
	for point in collisionPoints:
		(x,y) = point
		#grid-workable points are either negative (non-colliding)
		#positive and within 0-19 (numCells),
		#or 20+ (non-colliding on the right side)
		x = (x - offset)/numCells 
		y = (y - offset)/numCells
		modelPoint = (x,y)
		modelPoints.append(modelPoint)
	#evaluate collisions with only relevant grid rects
	for index, point in enumerate(modelPoints):
		#check if the bounds of the point warrant checking collision
		(x,y) = point #based on grid values...
		if (not((x < 0) or (x >= numCells)) and not((y < 0) or (y >= numCells))):
			#check collision
			if self.playfield.rectList[y][x]:
				if self.playfield.rectList[y][x].collidepoint(collisionPoints[index]): #uses actual point
					collision = True
				#set flag
	if (collision):
		thing.airborne = False
	else:
		thing.airborne = True

def checkFloor(self): #i wrote this
	testRect = thing.rect.move(0, 1)
	offset = 300 #screen pixels before grid in both x and y direction
	numCells = 20 #number of cells in a row/col of platform grid
	#un-converted values into list
	bottomleft = testRect.bottomleft
	bottomright = testRect.bottomright
	collisionPoints = [bottomleft, bottomright]
	modelPoints = []
	collision = False
	collideRects = []
	#mathematical conversion to grid model-workable values
	for point in collisionPoints:
		(x,y) = point
		#grid-workable points are either negative (non-colliding)
		#positive and within 0-19 (numCells),
		#or 20+ (non-colliding on the right side)
		x = (x - offset)/numCells 
		y = (y - offset)/numCells
		modelPoint = (x,y)
		modelPoints.append(modelPoint)
	#evaluate collisions with only relevant grid rects
	for index, point in enumerate(modelPoints):
		#check if the bounds of the point warrant checking collision
		(x,y) = point #based on grid values...
		if (not((x < 0) or (x >= numCells)) and not((y < 0) or (y >= numCells))):
			#check collision
			if self.playfield.rectList[y][x]:
				if self.playfield.rectList[y][x].collidepoint(collisionPoints[index]): #uses actual point
					collision = True
				#set flag
	if (collision):
		thing.airborne = False
	else:
		thing.airborne = True

def checkMove(self, thing):
	testRect = thing.rect.move(thing.xvel, thing.yvel)
	offset = 300 #screen pixels before grid in both x and y direction
	numCells = 20 #number of cells in a row/col of platform grid
	#un-converted values into list
	topleft = testRect.topleft
	topright = testRect.topright
	bottomleft = testRect.bottomleft
	bottomright = testRect.bottomright
	collisionPoints = [topleft, topright, bottomleft, bottomright]
	modelPoints = []
	collision = False
	collideRects = []
	#mathematical conversion to grid model-workable values
	for point in collisionPoints:
		(x,y) = point
		#grid-workable points are either negative (non-colliding)
		#positive and within 0-19 (numCells),
		#or 20+ (non-colliding on the right side)
		x = (x - offset)/numCells 
		y = (y - offset)/numCells
		modelPoint = (x,y)
		modelPoints.append(modelPoint)
	#evaluate collisions with only relevant grid rects
	for index, point in enumerate(modelPoints):
		#check if the bounds of the point warrant checking collision
		(x,y) = point #based on grid values...
		if (not((x < 0) or (x >= numCells)) and not((y < 0) or (y >= numCells))):
			#check collision
			if self.playfield.rectList[x][y].collidepoint(collisionPoints[index]): #uses actual point
				collision = True
				collideRects.append(self.playfield.rectList[x][y])
				#set flag
	if (collision):
		self.snapToSurface(thing, collisionPoints, collideRects)
	else:
		thing.move()

def snapToSurface(self, thing, collisionPoints, collisionRects):
	rectCorners = [thing.rect.topleft, thing.rect.topright, thing.rect.bottomleft, thing.rect.bottomright]
	#interpolations...
	pointA = self.interpolate(rectCorners[0], collisionPoints[0], collisionRects)
	pointB = self.interpolate(rectCorners[1], collisionPoints[1], collisionRects)
	pointC = self.interpolate(rectCorners[2], collisionPoints[2], collisionRects)
	pointD = self.interpolate(rectCorners[3], collisionPoints[3], collisionRects)
	interpolatedPoints = [pointA, pointB, pointC, pointD]
	#distance calculations...
	distA = self.distance(rectCorners[0], interpolatedPoints[0])
	distB = self.distance(rectCorners[1], interpolatedPoints[1])
	distC = self.distance(rectCorners[2], interpolatedPoints[2])
	distD = self.distance(rectCorners[3], interpolatedPoints[3])
	distances = [distA, distB, distC, distD]
	#snap relevant corner to shortest distanced interpolated point
	if (min(distances) == distA):
		thing.rect.topleft = pointA
	elif(min(distances) == distB):
		thing.rect.topright = pointB
	elif(min(distances) == distC):
		thing.rect.bottomleft = pointC
	elif(min(distances) == distD):
		thing.rect.bottomright = pointD
	else:
		assert(False) #should never get here!



def interpolate(self, origin, collision, rects): #return corrected point
	#determine which rect collides with the collisionPoint...
	rect = None
	for item in rects:
		if item.collidepoint(collision):
			rect = item
	#check trivial case: this point never collides anyway.
	if rect = None:
		return collision
	#interpolate to get the point on the surface of the rect we should snap to...(floats!)
	else:
		(x0, y0) = origin
		(x1, y1) = collision
		topline = rect.top
		bottomline = rect.bottom
		leftline = rect.left
		rightline = rect.right
	#Region I case - origin lies above platform
	if(y0 <= topline):
		if(x0 <= leftline):
			#hits left side of rect
			collisionSlope = self.slope(origin, collision)
			cornerSlope = self.slope(origin, rect.topleft)
			if (collisionSlope >= cornerSlope):
				yR = topline
				xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
			else:
				xR = leftline
				yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
		elif(leftline < x0 < rightline):
			#hits top of rect - trivial
			yR = topline
			xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
		else:
			#hits right side of rect
			collisionSlope = self.slope(origin, collision)
			cornerSlope = self.slope(origin, rect.topright)
			if(collisionSlope >= cornerSlope):
				xR = rightline
				yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
			else:
				yR = topline
				xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
	#Region II case - trivial - origin lies inbetween top and bottom of rectangle
	elif(topline < y0 < bottomline):
		if(x0 <= leftline):
			#hits left side of rect
			xR = leftline
			yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
		else:
			#hits right side of rect
			xR = rightline
			yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
	#Region III case - opposite I case - origin lies below platform
	else:
		if(x0 <= leftline):
			#hits left side of rect
			collisionSlope = self.slope(origin, collision)
			cornerSlope = self.slope(origin, rect.topright)
			if(collisionSlope >= cornerSlope):
				xR = leftline
				yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
			else:
				yR = bottomline
				xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
		elif(leftline < x0 < rightline):
			#hits bottom of rect
			yR = bottomline
			xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
		else:
			#hits right of rect
			collisionSlope = self.slope(origin, collision)
			cornerSlope = self.slope(origin, rect.topright)
			if(collisionSlope >= cornerSlope):
				yR = bottomline
				xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
			else:
				xR = rightline
				yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
	#return that point (as integers!)
	return (int(xR), int(yR))

def distance(self, point1, point2):
	#cast to floats!
	(x0, y0) = point1
	(x1, y1) = point2
	x0 = float(x0)
	y0 = float(y0)
	x1 = float(x1)
	y1 = float(y1)
	return(((x1 - x0)**2 + (y1 - y0)**2)**0.5)
	#returns a distance magnitude

def slope(self, point1, point2):
	#cast to floats!
	(x0,y0) = point1
	(x1,y1) = point2
	x0 = float(x0)
	y0 = float(y0)
	x1 = float(x1)
	y1 = float(y1)
	#formula...
	return (y1 - y0)/(x1 - x0)

def interpolationFormulaY(x0, y0, x1, y1, xR):
	#cast to floats!
	(x0,y0) = point1
	(x1,y1) = point2
	x0 = float(x0)
	y0 = float(y0)
	x1 = float(x1)
	y1 = float(y1)
	xR = float(xR)
	#formula...
	return (y0 + (y1 - y0)*((xR - x0)/(x1 - x0)))

def interpolationFormulaX(x0, y0, x1, y1, yR):
	#cast to floats!
	(x0,y0) = point1
	(x1,y1) = point2
	x0 = float(x0)
	y0 = float(y0)
	x1 = float(x1)
	y1 = float(y1)
	yR = float(yR)
	#formula...
	return (x0 + (x1 - x0)*((yR - y0)/(y1 - y0)))
