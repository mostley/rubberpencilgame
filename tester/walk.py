#!/usr/bin/python

import pygame,rabbyt
import os.path
from pygame.locals import *
size = (800,600)
rabbyt.data_directory = os.path.dirname(__file__)

class MovementDirection:
	NoWhere = 0
	Left = 1
	Right = 2
	Up = 4
	Down = 8

class GameObject(rabbyt.Sprite):
	def __init__(self, texture):
		rabbyt.Sprite.__init__(self, texture)

class Block(GameObject):
	def __init__(self, texture):
		GameObject.__init__(self, texture)

class Charactor(GameObject):
	lastFrameShift = 0
	spriteWidthFraction = 1.0/12.0
	width = 50
	height = 50
	speed = 20
	stepsize = 5.0
	nextMovementDirection = MovementDirection.NoWhere
	blocked = False
	
	def __init__(self, texture):
		GameObject.__init__(self, texture)
		self.tex_shape = [0,1,self.spriteWidthFraction,0]
		self.shape = [-self.width, self.height, self.width, -self.height]
	
	def update(self, dt):
		self.animate(dt)
		if not self.blocked:
			self.handleMovement(dt)
		else:
			self.blocked = False
	
	def isMovingNoWhere(self): return self.nextMovementDirection == MovementDirection.NoWhere
	def isMovingLeft(self): return (self.nextMovementDirection & MovementDirection.Left) == MovementDirection.Left
	def isMovingRight(self): return (self.nextMovementDirection & MovementDirection.Right) == MovementDirection.Right
	def isMovingUp(self): return (self.nextMovementDirection & MovementDirection.Up) == MovementDirection.Up
	def isMovingDown(self): return (self.nextMovementDirection & MovementDirection.Down) == MovementDirection.Down
	
	def animate(self, dt):
		if self.isMovingLeft():
			#charactor.texture = "img/char_left.png"
			self.shape = [self.width, self.height, -self.width, -self.height]
		elif self.isMovingRight():
			#charactor.texture = "img/char_right.png"
			self.shape = [-self.width, self.height, self.width, -self.height]
		#elif self.isMovingUp():
			#charactor.texture = "img/char_up.png"
		#elif self.isMovingDown():
			#charactor.texture = "img/char_down.png"
		
		if not self.isMovingNoWhere():
			if dt - self.lastFrameShift > 30:
				self.lastFrameShift = dt
				self.u += self.spriteWidthFraction
				if self.u > 1:
					self.u = self.spriteWidthFraction
	
	def handleMovement(self, dt):
		if self.isMovingLeft():
			self.x -= rabbyt.lerp(0,self.stepsize,dt=self.speed)
			
		elif self.isMovingRight():
			self.x += rabbyt.lerp(0,self.stepsize,dt=self.speed)
			
		if self.isMovingUp():
			self.y += rabbyt.lerp(0,self.stepsize,dt=self.speed)
			
		elif self.isMovingDown():
			self.y -= rabbyt.lerp(0,self.stepsize,dt=self.speed)
		

class Player(Charactor):
	def __init__(self, texture):
		Charactor.__init__(self, texture)
	
	def determineDirection(self):
		pressed = pygame.key.get_pressed()
		
		self.nextMovementDirection = MovementDirection.NoWhere
		if pressed[K_LEFT]:
			self.nextMovementDirection |= MovementDirection.Left
		if pressed[K_RIGHT]:
			self.nextMovementDirection |= MovementDirection.Right
		if pressed[K_UP]:
			self.nextMovementDirection |= MovementDirection.Up
		if pressed[K_DOWN]:
			self.nextMovementDirection |= MovementDirection.Down
		

class Enemy(Charactor):
	def __init__(self, texture):
		Charactor.__init__(self, texture)
	
	def determineDirection(self):
		pass


pygame.init()
screen = pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)
#rabbyt.set_viewport((0,0,size[0],size[1]),(0,0,size[0],-size[1]))
rabbyt.set_viewport(size)
rabbyt.set_default_attribs()

sprites = []

player = Player("img/char_sheet.png")
player.x, player.y = 100,100
sprites.append(player)

#block = Block("img/block.png")
#block.x,block.y = 400,400
#sprites.append(block)

running = True
clock = pygame.time.Clock()
while running:
	dt = pygame.time.get_ticks()
	rabbyt.set_time(dt)
	
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
	
	player.determineDirection()
	
	collisions = rabbyt.collisions.aabb_collide(sprites)
	
	for group in collisions:
		block = None
		if group[0] == player:
			block = group[1]
		else:
			block = group[0]
		
		block.rgb = rabbyt.lerp((1,0,0),(1,1,1), dt=.4)
		
		#move up
		print str(player.bottom > block.top) + " " + str(player.bottom < block.bottom) + " " + str(player.top < block.top)
		print str(player.bottom) + " " + str(player.top) + " " + str(block.bottom) + " " + str(block.top)
		if player.bottom > block.top and player.bottom < block.bottom and player.top < block.top:
			print "aa"
			player.y += player.bottom - block.top
		
		#if player.left < block.right and player.left > block.left:
		#	player.x += block.right - player.left
		#elif player.right > block.left and player.right < block.right:
		#	player.x += block.left - player.right
		#elif player.top < block.bottom and player.top > block.top:
		#	player.y += block.bottom - player.top
		#elif player.bottom > block.top and player.bottom < block.bottom:
		#	player.y += block.top - player.bottom
	
	for s in sprites:
		if isinstance(s, Charactor):
			s.update(dt)
	
	rabbyt.clear((255,255,255))
	rabbyt.render_unsorted(sprites)
	pygame.display.flip()
