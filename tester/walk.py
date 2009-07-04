#!/usr/bin/python

import pygame,rabbyt
import os.path
from pygame.locals import *
size = (800,600)
rabbyt.data_directory = os.path.dirname(__file__)


pygame.init()
screen = pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)
rabbyt.set_viewport(size)
rabbyt.set_default_attribs()

charactor = rabbyt.Sprite("img/char.png")

def changefacingDirection(pressed, charactor):
	if pressed[K_LEFT]:
		charactor.texture = "img/char_left.png"
	elif pressed[K_RIGHT]:
		charactor.texture = "img/char_right.png"
	#elif pressed[K_UP]:
		#charactor.texture = "img/char_up.png"
	#elif pressed[K_DOWN]:
		#charactor.texture = "img/char_down.png"

def handlemovement(pressed, charactor):
	dt = 20
	dist = 15.0
	if pressed[K_LEFT]:
		charactor.x -= rabbyt.lerp(0,dist,dt=dt)
	if pressed[K_RIGHT]:
		charactor.x += rabbyt.lerp(0,dist,dt=dt)
	if pressed[K_UP]:
		charactor.y += rabbyt.lerp(0,dist,dt=dt)
	if pressed[K_DOWN]:
		charactor.y -= rabbyt.lerp(0,dist,dt=dt)

running = True
clock = pygame.time.Clock()
while running:
	rabbyt.set_time(pygame.time.get_ticks())
	
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
	
	pressed = pygame.key.get_pressed()
	changefacingDirection(pressed, charactor)
	handlemovement(pressed, charactor)
	
	rabbyt.clear((255,255,255))
	#rabbyt.clear()
	
	charactor.render()
	
	pygame.display.flip()
