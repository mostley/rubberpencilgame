#!/usr/bin/python

import random,pygame,math,time,rabbyt
from model.creature import Creature
from visualizer import Visualizer
from postman import Postman
from states.statemachine import Statemachine
from states.menustate import MenuState
from pygame.locals import *

if pygame.font == None: print "no fonts!"

class Main:
	isRunning = False
	visualizer = None
	postman = None
	statemachine = None
	
	def __init__(self):
		self.visualizer = Visualizer(self)
		self.postman = Postman(self)
		
		self.statemachine = Statemachine(self)
		self.statemachine.append(MenuState(self.statemachine))
	
	def run(self):
		self.isRunning = True
		
		while(self.isRunning):
			self.postman.walk()
			
			dt = pygame.time.get_ticks()/1000.0
			rabbyt.set_time(dt)
		
			self.statemachine.update(dt)
			
			self.visualizer.draw(self.statemachine, dt)

if __name__ == "__main__":
	main = Main()
	main.run()

