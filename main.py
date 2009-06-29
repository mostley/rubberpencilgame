#!/usr/bin/python

import random,pygame,math,time,rabbyt
from model.creature import Creature
from visualizer import Visualizer
from postman import Postman
from states.statemachine import Statemachine
from states.menustate import MenuState
from pygame.locals import *
from pgu import tilevid, timer, gui

if pygame.font == None: print "no fonts!"

class Main:
	isRunning = False
	visualizer = None
	postman = None
	statemachine = None
	tileengine = None
	maps = []
	currentlevel = -1
	
	def __init__(self):
		self.visualizer = Visualizer(self)
		self.tileengine = tilevid.Tilevid()
		self.postman = Postman(self)
		
		self.statemachine = Statemachine(self)
		self.statemachine.push(MenuState(self.statemachine))
		
		self.loadMapNames()
	
	def loadMapNames(self):
		mapfile = file('data/levels.dat', 'r')
		for line in mapfile:
			self.maps.append(line)
	
	def loadNextLevel():
		self.currentlevel += 1
		if self.currentlevel >= 0:
			self.statemachine.pop()
		
		self.statemachine.push(MapState(self.maps[self.currentlevel]))
	
	def run(self):
		self.isRunning = True
		
		while(self.isRunning):
			self.postman.walk()
			
			dt = pygame.time.get_ticks()/1000.0
			rabbyt.set_time(dt)
		
			self.statemachine.update(dt)
			
			#self.tileengine.loop()
			self.visualizer.draw(self.statemachine, dt)
			
			#updates = self.tileengine.update(self.tileengine.screen)
			#pygame.display.update(updates)
		
		
		self.visualizer.quit()
		self.tileengine.quit = 1

if __name__ == "__main__":
	main = Main()
	main.run()

