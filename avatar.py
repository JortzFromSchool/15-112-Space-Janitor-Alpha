#avatarphysics v.0.1

import pygame as pg

class Avatar(object):
	def __init__(self, screen, screenLength, screenWidth, height = 18, width = 18):
		self.screenLength = screenLength
		self.screenWidth = screenWidth
		self.screen = screen
		self.height = height
		self.width = width
		self.grav = 0.22
		self.maxy = 20
		self.maxSpeed = 6
		self.speed = 4 #implement momentum?
		self.xvel = self.yvel = 0
		self.jumpAcc = -8.5
		self.jump_cut_mag = 4
		self.isMelee = False
		self.airborne = True
		self.facingLeft = True
		self.doubleJumpReady = False
		self.airborneUpRelease = False
		self.rect = pg.Rect(screenLength/2-self.width, 40, self.height, self.width)
		self.meleeRect = self.rect.move(-self.width, 0)
		self.flagTopLeft = False
		self.flagTopRight = False
		self.flagBottomLeft = False
		self.flagBottomRight = False
		self.wallLeft = False
		self.wallRight = False
		self.capped = False
		#self.image = pg.image.load("avatar.png").convert()
		self.goombaStomp = True

	def init(self):
		self.grav = 0.22
		self.maxSpeed = 6
		self.speed = 4 #implement momentum?
		self.xvel = self.yvel = 0
		self.jumpAcc = -12.5
		self.jump_cut_mag = 4
		self.isMelee = False
		self.airborne = True
		self.facingLeft = True
		self.doubleJumpReady = False
		self.airborneUpRelease = False
		self.rect = pg.Rect(self.screenLength/2-self.width, 40, self.height, self.width)
		self.meleeRect = self.rect.move(-self.width, 0)
		self.flagTopLeft = False
		self.flagTopRight = False
		self.flagBottomLeft = False
		self.flagBottomRight = False
		self.wallLeft = False
		self.wallRight = False

	def jump(self):
		if not(self.airborne):
			self.yvel = self.jumpAcc
			self.airborne = True
			self.doubleJumpReady = True
		elif(self.doubleJumpReady and self.airborneUpRelease):
			self.doubleJumpReady = False
			self.doubleJump()

	def doubleJump(self):
		self.yvel = self.jumpAcc

	def melee(self):
		self.isMelee = True
		if(self.facingLeft):
			self.meleeLeft
		else:
			self.meleeRight()

	def meleeLeft(self):
		self.meleeRect = self.rect.move(-self.width,0)

	def meleeRight(self):
		self.meleeRect = self.rect.move(self.width,0)

	def updateMeleeBox(self):
		if self.isMelee:
			if self.facingLeft:
				self.meleeRect = self.rect.move(-self.width,0)
			else:
				self.meleeRect = self.rect.move(self.width,0)

	def throwGrenade(self):
		pass

	def jumpCut(self):#CITATION GOES TO Sean J. McKiernan 'Mekire'
		if self.airborne:
			if self.yvel < self.jump_cut_mag:
				self.yvel = self.jump_cut_mag

	def checkKeys(self, keys):#CITATION GOES TO Sean J. McKiernan 'Mekire'
		self.x_vel = 0
		if keys[pg.K_RIGHT]:
			self.xvel += self.speed
			if self.xvel > self.maxSpeed:
				self.xvel = self.maxSpeed
			self.facingLeft = False
		elif keys[pg.K_LEFT]:
			self.xvel -= self.maxSpeed
			if self.xvel < -self.maxSpeed:
				self.xvel = -self.maxSpeed
			self.facingLeft = True
		elif keys[pg.K_r]:
			self.init()
		else:
			if(self.xvel > 0):
				self.xvel -= 2
			elif (self.xvel < 0):
				self.xvel += 2

	def physicsUpdate(self):
		if self.capped:
			if self.yvel > 0:
				self.yvel = 0
		if self.airborne:
			self.yvel += self.grav
			if self.yvel >= self.maxy:
				self.yvel = self.maxy
		else:
			self.yvel = 0
		if self.wallLeft and self.xvel < 0:
			self.xvel = 0
		if self.wallRight and self.xvel >0:
			self.xvel = 0
		if not(self.isMelee):
			self.meleeRect = None

	def move(self):
		self.rect.move_ip(self.xvel, self.yvel)

	def update(self, keys):
		self.checkKeys(keys)
		self.physicsUpdate()
		self.updateMeleeBox()

	def draw(self):
		pg.draw.rect(self.screen, (255, 100, 0), self.rect)
		#if self.facingLeft:
		#	self.screen.blit(self.image, self.rect)
		#else:
		#	image = pg.transform.flip(self.image, True, False)
		#	self.screen.blit(image, self.rect)
		if self.isMelee:
			pg.draw.rect(self.screen, (255, 0, 100), self.meleeRect, 3)

