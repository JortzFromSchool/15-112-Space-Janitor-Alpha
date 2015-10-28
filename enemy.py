#enemy.py
#here's the code for the buggies in the game. It is based off my own player class.

import pygame as pg
import random

class Bug(object):
	def __init__(self, screen, screenLength, screenWidth, x, y, height = 15, width = 15):
		self.offset = 300
		self.screenLength = screenLength
		self.screenWidth = screenWidth
		self.screen = screen
		self.height = height
		self.width = width
		self.grav = 0.22
		self.speed = 1
		self.xvel = self.yvel = 0
		self.airborne = True
		self.facingLeft = False
		seed = random.randint(0,1)
		if seed == 1:
			self.facingLeft = True
		self.rect = pg.Rect(x, y, self.height, self.width)
		self.eatRect = None
		self.flagTopLeft = False
		self.flagTopRight = False
		self.flagBottomLeft = False
		self.flagBottomRight = False
		self.wallLeft = False
		self.wallRight = False
		self.capped = False
		self.health = 1
		self.value = 5 #points
		self.full = None
		self.eatTimer = 60 #milliseconds
		self.oldEatTimer = 121
		self.eatOrder = 0
		self.eatStates = 3
		self.blocksEaten = 0

	def hunger(self):
		self.eatTimer -= 1

	def eatDown(self):
		self.eatRect = None
		if self.eatTimer < 1:
			self.eatRect = pg.Rect(self.rect.x, self.rect.y+self.height, 20, 20)
			self.eatTimer = self.oldEatTimer
			self.eatOrder += 1

	def eatLeft(self):
		self.eatRect = None
		if self.eatTimer < 1:
			self.eatRect = pg.Rect(self.rect.x + self.height, self.rect.y, 20, 20) #fix magic Numbers!
			self.eatTimer = self.oldEatTimer
			self.eatOrder += 1

	def eatRight(self):
		self.eatRect = None
		if self.eatTimer < 1:
			self.eatRect = pg.Rect(self.rect.x - self.height, self.rect.y, 20, 20) #fix magic Numbers!
			self.eatTimer = self.oldEatTimer
			self.eatOrder += 1


	def physicsUpdate(self):
		if(self.facingLeft):
			if self.wallLeft:
				self.rect.move(1,0)
				self.xvel = self.speed
				self.facingLeft = False
			else:
				self.xvel = -self.speed
		else:
			if self.wallRight:
				self.xvel = -self.speed
				self.facingLeft = True
			else:
				self.xvel = self.speed
		if self.airborne:
			self.yvel += self.grav
			self.xvel = 0
		else:
			self.yvel = 0
		eatCommand = self.eatOrder%self.eatStates
		if (self.eatTimer <= 0):
			if(eatCommand == 0):
				self.eatDown()
			elif(eatCommand == 1):
				self.eatLeft()
			else:
				self.eatRight()

	def move(self):
		if(self.rect.x + self.xvel) < self.offset:#300
			self.rect.left = self.offset + 1
			self.xvel = -self.xvel
			self.facingLeft = not(self.facingLeft)
		elif(self.rect.x + self.xvel) > self.screenLength - self.offset-5:#700s
			self.rect.right = (self.screenLength - self.offset) - 1
			self.xvel = -self.xvel
			self.facingLeft = not(self.facingLeft)
		else:
			self.rect.move_ip(self.xvel, self.yvel)

	def update(self):
		self.physicsUpdate()
		self.draw()


	def draw(self):
		pg.draw.rect(self.screen, (100, 255, 0), self.rect)
		if self.eatRect:
			pg.draw.rect(self.screen, (100, 100, 255), self.eatRect, 3)