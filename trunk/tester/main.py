#!/usr/bin/python

import rabbyt
from pyglet.window import Window
from pyglet.window import key
from pyglet import clock
from pyglet.gl import *
from math import *
import os.path
from pyglet import font

from enums import *
from gameobjects import *
from spritetext import *
from camera import *


class Main(Window):
	objects = []
	sprites = []
	player = None
	textsprite = None
	keyboardHandler = None
	camera = None
	
	def __init__(self, size):
		Window.__init__(self, width=size[0], height=size[1])
		
		self.camera = Camera((size[0]/2.0, size[1]/2.0))
		self.on_resize = self.camera.view
		self.on_mouse_drag = self.camera.drag
		
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
			if group[0].parent == player:
				block = group[1]
			else:
				block = group[0]
			
			block.rgb = rabbyt.lerp((1,0,0),(1,1,1), dt=.4)
			
		
		for obj in self.objects:
			if isinstance(obj, Charactor):
				obj.update(dt)
		
		if self.keyboardHandler[key.SPACE]: self.camera.reset()
	
	def drawGrid(self):
		pyglet.gl.glColor3f(0.0, 0.0, 0.0) # set color to black
		lines = (0, 0, 
				 640, 480,
				 640, 0,
				 0, 480,
				 320, 0,
				 320, 480,
				 0, 240,
				 640, 240,
				 0,0,
				 640,0,
				 640,0,
				 640,480,
				 640,480,
				 0,480,
				 0,480,
				 0,0)
		pyglet.graphics.draw(len(lines)/2, pyglet.gl.GL_LINES, ('v2i', lines))
	
	def draw(self, dt):
		for obj in self.objects:
			obj.render(dt)
		
		self.textsprite.render()
		
		self.drawGrid()
	
	def run(self):
		while not self.has_exit:
			dt = clock.tick()
			self.dispatch_events()
			
			self.camera.update(dt)
			self.camera.apply()
			
			self.updateModel(dt)
			
			rabbyt.clear((255,255,255))
			
			self.draw(dt)
			
			self.flip()
	
	# == Event Handling ==
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if scroll_y > 0:
			self.camera.zoomIn()
		elif scroll_y < 0:
			self.camera.zoomOut()

if __name__ == "__main__":
	size = (640, 480)
	
	main = Main(size)

	player = Player("img/char_sheet.png")
	main.addObject(player, (100,100))

	block = Block("img/block.png")
	main.addObject(block, (400,400))
	
	main.run()
