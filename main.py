"""
Citation: modified version of Sean J. McKiernan's 'Mekire'
main class found in his application "platformer with slopes,"
which in general was used to decipher Pygame platforming. Modifications
include variable value changes, changes to the level imported,
changes to the avatar imported, and more controls added.

ALL COLLISION DETECTION CODE IS MY OWN. AND IT TOOK FOREVER! YAY!
THE ONLY CODE THAT IS NOT MINE IS DESIGNATED AS SUCH.
"""

import os
import sys
import random
import pygame as pg
from playField import PlayField
from avatar import Avatar
from pygame.locals import *
from enemy import Bug

class Control(object):#MODIFIED VERSION OF Mekire's CONTROL __INIT__ FUNCTION
	"""Primary control flow."""
	def __init__(self):
		"""Initialize the display and create a player and level."""
		self.screen = pg.display.set_mode((1000,1000))
		self.screen_rect = self.screen.get_rect()
		self.clock = pg.time.Clock()
		self.fps = 60.0
		self.keys = pg.key.get_pressed()
		self.done = False
		self.playfield = PlayField(1000, 1000,20,20,self.screen)
		self.avatar = Avatar(self.screen, 1000, 1000)
		self.bugList = []
		self.score = 0
		pg.display.set_caption('Space Custodian Alpha')

		# scoring variables
		self.score = 0
		self.msg = "Score: %d" % self.score
		self.fontObj = pg.font.Font('freesansbold.ttf', 18)
		self.msgSurface = self.fontObj.render(self.msg, False, (0,0,255))
		self.msgRect = self.msgSurface.get_rect()

		#visual timing variables
		self.timer = 0
		self.timerMsg= "%d seconds alive." % self.timer
		self.timerSurface = self.fontObj.render(self.timerMsg, False, (100, 0, 255))
		self.timerRect =  self.timerSurface.get_rect()

		#visual instructions variables
		self.instructions = "Arrow Keys to Move. Space to (Double Jump). R to warp. X to melee. Don't let too many bugs get to the bottom!"
		self.instructionSurface = self.fontObj.render(self.instructions, False, (100,100,100))
		self.instructionRect = self.instructionSurface.get_rect()


		self.bugSpawnThreshold = 60 # frames
		self.bugSpawnTimer = 0
		self.lifepoints = 20
		self.gameOver = False
		self.highScore = 0

	def manageLifepoints(self):
		for bug in self.bugList:
			if (bug.rect.y >= 800):
				trash = self.bugList.remove(bug)
				self.lifepoints -= 1
		if (self.lifepoints <= 0):
			if self.score > self.highScore:
				self.highScore = self.score
			self.msg = "Game Over! Score: %d HighScore: %d (press press t to restart!)" % (self.score, self.highScore)
			self.msgSurface = self.fontObj.render(self.msg, False, (0,0,255))
			self.msgRect = self.msgSurface.get_rect()
			self.msgRect.topleft = (250, 250)
			self.screen.blit(self.msgSurface, self.msgRect)
			self.gameOver = True

	def event_loop(self): #modified from original version for my keyset
		"""Let us quit and jump."""
		for event in pg.event.get():
			self.keys = pg.key.get_pressed()
			if self.gameOver:
				if self.keys[pg.K_t]:
					self.restart()
			if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
				self.done = True
			elif self.keys[pg.K_x]:
				self.avatar.melee()
			elif self.keys[pg.K_c]:
				self.avatar.throwGrenade()
			#elif self.keys[pg.K_b]:
			#	newBug = Bug(self.screen, 1000, 1000, random.randint(250, 750-15), 40)
			#	self.bugList.append(newBug)
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.avatar.jump()
			elif event.type == pg.KEYUP:
				if event.key == pg.K_x:
					self.avatar.isMelee = False
				if event.key == pg.K_SPACE:
					self.avatar.jumpCut()
					if (self.avatar.airborne):
						self.avatar.airborneUpRelease = True

	def restart(self):
		self.screen = pg.display.set_mode((1000,1000))
		self.screen_rect = self.screen.get_rect()
		self.clock = pg.time.Clock()
		self.fps = 60.0
		self.keys = pg.key.get_pressed()
		self.done = False
		self.playfield = PlayField(1000, 1000,20,20,self.screen)
		self.avatar = Avatar(self.screen, 1000, 1000)
		self.bugList = []
		self.score = 0
		pg.display.set_caption('Space Custodian Alpha Build')

		# scoring variables
		self.score = 0
		self.msg = "Score: %d" % self.score
		self.fontObj = pg.font.Font('freesansbold.ttf', 20)
		self.msgSurface = self.fontObj.render(self.msg, False, (0,0,255))
		self.msgRect = self.msgSurface.get_rect()

		#visual timing variables
		self.timer = 0
		self.timerMsg= "%d seconds alive." % self.timer
		self.timerSurface = self.fontObj.render(self.timerMsg, False, (100, 0, 255))
		self.timerRect = self.timerSurface.get_rect()

		#visual instructions variables
		self.instructions = "Arrow Keys to Move. Space to Jump/Double Jump. R to warp to top. X to melee. Don't let too many bugs get to the bottom!"
		self.instructionSurface = self.fontObj.render(self.instructions, False, (100,100,100))
		self.instructionRect = self.instructionSurface.get_rect()


		self.bugSpawnThreshold = 60 # frames
		self.bugSpawnTimer = 0
		self.lifepoints = 20
		self.gameOver = False

	def updateMsgs(self):
		self.timer += 1

		# score
		self.msg = "Score: %d" % self.score
		self.msgSurface = self.fontObj.render(self.msg, False, (0,0,255))
		self.msgRect = self.msgSurface.get_rect()
		self.msgRect.topleft = (10, 25)
		self.screen.blit(self.msgSurface, self.msgRect)

		# time
		self.timerMsg= "%d seconds alive." % (self.timer/int(self.fps))
		self.timerSurface = self.fontObj.render(self.timerMsg, False, (100, 0, 255))
		self.timerRect.topleft = (10, 50)
		self.screen.blit(self.timerSurface, self.timerRect) 

		# instructions
		self.instructionRect.topright = (995, 5)
		self.screen.blit(self.instructionSurface, self.instructionRect)


	#################
	# BUG METHODS - ALL ORIGINAL WORK
	#################

	def generateBug(self):
		if(self.bugSpawnTimer>=self.bugSpawnThreshold):
			newBug = Bug(self.screen, 1000, 1000, random.randint(250, 750-15), 40)
			self.bugList.append(newBug)
			self.bugSpawnTimer = 0
			self.bugSpawnThreshold = random.randint(0,2)*60 #seconds * frames
		else:
			self.bugSpawnTimer += 1

	def updateBugList(self):
		for bug in self.bugList:
			if bug.health < 1:
				trash = self.bugList.remove(bug)
			elif bug.rect.centery >= 1000:
				trash = self.bugList.remove(bug)

	def checkBugEatCollisions(self, bug):
		testRect = bug.eatRect
		if (testRect == None): #base case
			return
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
						self.playfield.rectList[y][x] = None
						bug.blocksEaten += 1

	#################
	# AVATAR COLLISION - ALL ORIGINAL WORK
	#################

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
			#print index, point
			#check if the bounds of the point warrant checking collision
			(x,y) = point #based on grid values...
			if (not((x < 0) or (x >= numCells)) and not((y < 0) or (y >= numCells))):
				#check collision
				#print index, "point =", collisionPoints[index]
				#print self.playfield.rectList[y][x].topleft
				if self.playfield.rectList[y][x]:
					if self.playfield.rectList[y][x].collidepoint(collisionPoints[index]): #uses actual point
						collision = True
						collideRects.append(self.playfield.rectList[y][x])
		# print "collisionRect Coords:"
		# for item in collideRects:
		# 	print item.topleft
		if (collision):
			thing.xvel = 0
			self.snapToSurface(thing, collisionPoints, collideRects)
		else:
			thing.move()
		self.checkFloor(thing)
		self.checkWalls(thing)

	def snapToSurface(self, thing, collisionPoints, collisionRects):
		# print "(300, 480)" #first two coords w/o movement
		# print "(300, 500)"
		# print "snapToSurface called."
		# print "collisionPoints;"
		# for item in collisionPoints:
		# 	print item
		# print "Corners:"
		rectCorners = [thing.rect.topleft, thing.rect.topright, thing.rect.bottomleft, thing.rect.bottomright]
		# for corner in rectCorners:
		# 	print corner
		#interpolations...
		# print "interpolations:"
		pointA = self.interpolate(rectCorners[0], collisionPoints[0], collisionRects, thing)
		pointB = self.interpolate(rectCorners[1], collisionPoints[1], collisionRects, thing)
		pointC = self.interpolate(rectCorners[2], collisionPoints[2], collisionRects, thing)
		pointD = self.interpolate(rectCorners[3], collisionPoints[3], collisionRects, thing)
		interpolatedPoints = [pointA, pointB, pointC, pointD]
		# for interpoint in interpolatedPoints:
		# 	print interpoint
		#distance calculations...
		# print "distances:"
		distA = self.distance(rectCorners[0], interpolatedPoints[0])
		distB = self.distance(rectCorners[1], interpolatedPoints[1])
		distC = self.distance(rectCorners[2], interpolatedPoints[2])
		distD = self.distance(rectCorners[3], interpolatedPoints[3])
		distances = [distA, distB, distC, distD]
		# for dists in distances:
		# 	print dists
		#snap relevant corner to shortest distanced interpolated point
		# print "minimum dist =", min(distances)
		distances.sort()
		for item in distances:
			if (item == distA):
				thing.rect.topleft = pointA
				# print "Min point A"
			elif(item == distB):
				# print "Min point B"
				thing.rect.topright = pointB
			elif(item == distC):
				# print "Min point C"
				thing.rect.bottomleft = pointC
			else: #item == distD
				# print "Min point D"
				thing.rect.bottomright = pointD
			fixed = True
			for obstacle in collisionRects:
				if obstacle.colliderect(thing.rect):
					fixed = False
			if fixed:
				return

	def interpolate(self, origin, collision, rects, thing): #return corrected point
		#determine which rect collides with the collisionPoint...
		rect = None
		for item in rects:
			if item.collidepoint(collision):
				rect = item
		#check trivial case: this point never collides anyway.
		if rect == None:
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
			#print "interpolation Region I achieved!"
			if(x0 < leftline):
				#hits left side of rect
				collisionSlope = self.slope(origin, collision)
				#print "collisionSlope: ", collisionSlope
				cornerSlope = self.slope(origin, rect.topleft)
				#print "cornerSlope:", cornerSlope
				if (collisionSlope >= cornerSlope):
					#print "hits top"
					yR = topline-1
					xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
					thing.yvel = 0
					thing.airborne = False
				else:
					#print "hits left"
					xR = leftline-1
					yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
			elif(leftline <= x0 <= rightline):
				#hits top of rect - trivial
				yR = topline-1
				xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
				thing.yvel = 0
				thing.airborne = False
			else:
				#hits right side of rect
				collisionSlope = self.slope(origin, collision)
				cornerSlope = self.slope(origin, rect.topright)
				if(collisionSlope >= cornerSlope):
					xR = rightline+1
					yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
				else:
					yR = topline-1
					xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
					thing.yvel = 0
					thing.airborne = False
		#Region II case - trivial - origin lies inbetween top and bottom of rectangle
		elif(topline < y0 < bottomline):
			#print "interpolation Region II achieved!"
			if(x0 <= leftline):
				#hits left side of rect
				xR = leftline-1
				yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
			else:
				#hits right side of rect
				xR = rightline+1
				yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
		#Region III case - opposite I case - origin lies below platform
		else:
			#print "interpolation Region I achieved!"
			if(x0 < leftline):
				#hits left side of rect
				collisionSlope = self.slope(origin, collision)
				cornerSlope = self.slope(origin, rect.topright)
				if(collisionSlope >= cornerSlope):
					xR = leftline-1
					yR = self.interpolationFormulaY(x0, y0, x1, y1, xR)
				else:
					yR = bottomline+1
					xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
			elif(leftline <= x0 <= rightline):
				#hits bottom of rect
				yR = bottomline+1
				xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
			else:
				#hits right of rect
				collisionSlope = self.slope(origin, collision)
				cornerSlope = self.slope(origin, rect.topright)
				if(collisionSlope >= cornerSlope):
					yR = bottomline+1
					xR = self.interpolationFormulaX(x0, y0, x1, y1, yR)
				else:
					xR = rightline+1
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
		if (x1 - x0 == 0):
			x1 += 0.000001
		return (y1 - y0)/(x1 - x0)

	def interpolationFormulaY(self, x0, y0, x1, y1, xR):
		#cast to floats!
		x0 = float(x0)
		y0 = float(y0)
		x1 = float(x1)
		y1 = float(y1)
		xR = float(xR)
		if(x1 - x0 == 0):
			return x0
		#formula...
		return (y0 + (y1 - y0)*((xR - x0)/(x1 - x0)))

	def interpolationFormulaX(self, x0, y0, x1, y1, yR):
		#cast to floats!
		x0 = float(x0)
		y0 = float(y0)
		x1 = float(x1)
		y1 = float(y1)
		yR = float(yR)
		if(y1-y0 == 0):
			return y0
		#formula...
		return (x0 + (x1 - x0)*((yR - y0)/(y1 - y0)))

	def checkCeiling(self, thing): #i wrote this
		testRect = thing.rect.move(0, -1)
		offset = 300 #screen pixels before grid in both x and y direction
		numCells = 20 #number of cells in a row/col of platform grid
		#un-converted values into list
		topleft = testRect.topleft
		topright = testRect.topright
		collisionPoints = [topleft, topright]
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
			thing.capped = False
		else:
			thing.capped = True

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

	def checkRight(self, thing): #i wrote this
		testRect = thing.rect.move(1,0)
		offset = 300 #screen pixels before grid in both x and y direction
		numCells = 20 #number of cells in a row/col of platform grid
		#un-converted values into list
		topright = testRect.topright
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
		topleft = testRect.topleft
		bottomleft = testRect.bottomleft
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
		self.checkLeft(thing)
		self.checkRight(thing)

	def checkMeleeCollisions(self):
		if (self.avatar.isMelee):
			for bug in self.bugList:
				if self.avatar.meleeRect.colliderect(bug.rect):
					bug.health -= 1
					self.score += 5 + bug.blocksEaten

	def checkPlayerKillzone(self):
		if self.avatar.rect.y >= 800:
			self.avatar.rect = pg.Rect(self.avatar.screenLength/2-self.avatar.width, 
				40, self.avatar.height, self.avatar.width)


####
#ALL CODE BELOW IS MODIFIED CODE FROM Mekire's CONTROL CLASS
#####
	def update(self): 
		if not(self.gameOver):
			"""Call the update for the level and the actors."""
			self.screen.fill((140,140,255))
			self.avatar.update(self.keys)
			self.playfield.update()
			self.checkMove(self.avatar)
			self.checkMeleeCollisions()
			self.avatar.draw()
			for bug in self.bugList:
				bug.update()
				bug.draw()
				bug.hunger()
				self.checkMove(bug)
				self.checkBugEatCollisions(bug)
			self.generateBug()
			self.playfield.update()
			self.updateBugList()
			self.checkPlayerKillzone()
			self.avatar.draw()
			self.updateMsgs()
			self.manageLifepoints()


#######
#ALL CODE BELOW IS ALMOST DIRECTLY FROM mekire's CONTROL CLASS
#######
	def main_loop(self):
		"""Run around."""
		while not self.done:
			self.event_loop()
			self.update()
			pg.display.update()
			self.clock.tick(self.fps)

if __name__ == "__main__":
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pg.init()
	screenSize = 1000
	pg.display.set_mode((screenSize , screenSize))
	run_it = Control()
	run_it.main_loop()
	pg.quit()
	sys.exit()
