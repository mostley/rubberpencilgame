import pygame
from pygame.locals import *

class Postman:
	main = None
	
	def __init__(self, main):
		self.main = main
	
	def walk(self):
		for e in pygame.event.get():
			if e.type == QUIT:
				self.main.isRunning = False
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					self.main.isRunning = False
