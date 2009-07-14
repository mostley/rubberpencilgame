#!/usr/bin/python

import rabbyt
from pyglet.window import Window
from pyglet.window import key
from pyglet import clock
import os.path
from pyglet import font

from enums import *
from gameobjects import *
from spritetext import *

class Main(Window):
	objects = []
	sprites = []
	size = (800,600)
	player = None
	textsprite = None
	keyboardHandler = None
	
	def __init__(self, size):
		Window.__init__(self, width=size[0], height=size[1])
		
		self.size = size
		
		clock.schedule(rabbyt.add_time)
		clock.set_fps_limit(60)
		
		rabbyt.set_default_attribs()
		rabbyt.data_directory = os.path.dirname(__file__)
		
		self.keyboardHandler = key.KeyStateHandler()
		self.push_handlers(self.keyboardHandler)

		
		ft = font.load('Arial', 24)
		self.textsprite = SpriteText(ft, "Hello World", xy=(320,240))
		self.textsprite.rot = rabbyt.lerp(0,360, dt=5, extend="extrapolate")
		self.textsprite.rgb = rabbyt.lerp((1,0,0), (0,1,0), dt=2, extend="reverse")
		
	
	def addObject(self, obj, pos):
		obj.setPosition(pos)
		self.objects.append(obj)
		spritelist = obj.getSprites()
		for s in spritelist:
			self.sprites.append(s)
		if isinstance(obj, Player):
			self.player = obj
	
	def updateModel(self, dt):
		self.player.determineDirection(self.keyboardHandler)
		
		collisions = rabbyt.collisions.aabb_collide(self.sprites)
		
		for group in collisions:
			block = None
			if group[0] == player:
				block = group[1]
			else:
				block = group[0]
			
			print "peng"
			block.rgb = rabbyt.lerp((1,0,0),(1,1,1), dt=.4)
			
		
		for obj in self.objects:
			if isinstance(obj, Charactor):
				obj.update(dt)
	
	def draw(self, dt):
		for obj in self.objects:
			obj.render(dt)
		
		self.textsprite.render()
	
	def run(self):
		while not self.has_exit:
			dt = clock.tick()
			self.dispatch_events()
			
			self.updateModel(dt)
			
			rabbyt.clear((255,255,255))
			
			self.draw(dt)
			
			self.flip()
	
	# == Event Handling ==
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		pass

if __name__ == "__main__":
	size = (640, 480)
	
	main = Main(size)

	player = Player("img/char_sheet.png")
	main.addObject(player, (100,100))

	block = Block("img/block.png")
	main.addObject(block, (400,400))
	
	main.run()
