#!/usr/bin/python

import rabbyt, pyglet
from pyglet.window import Window 
import os.path

import from enums import *
import from gameobjects import *

class Main(pyglet.window.Window):
	#screen = None
	objects = []
	sprites = []
	running = False
	size = (800,600)
	window = None
	player = None
	
	def __init__(self, size, window):
		pyglet.window.Window.__init__(self, width=size[0], height=size[1])
		self.size = size
		self.window = window
		
		#rabbyt.set_viewport((size[0],size[1]), projection=(0,0,size[0],size[1]))
		rabbyt.set_default_attribs()
		
		pyglet.clock.schedule(rabbyt.add_time)
		rabbyt.data_directory = os.path.dirname(__file__)
	
	def addObject(self, obj, pos):
		obj.SetPosition(pos)
		self.objects.append(obj)
		spritelist = obj.GetSprites()
		for s in spritelist:
			self.sprites.append(s)
		if isinstance(obj, Player):
			self.player = obj
	
	def update(self, dt):
		self.player.determineDirection()
		
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
		
		rabbyt.clear((255,255,255))
		for obj in self.objects:
			obj.render(dt)
	#pyglet.gl.glColor3f(0.0, 0.0, 0.0) # set color to black
	#pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (10, 15, 30, 35)) )
	
	def run(self):
		pyglet.app.run() 
	
	# == Event Handling ==
	
	def on_key_press(self, symbol, modifiers):
		pass

	def on_key_release(self, symbol, modifiers):
		pass
	
	def on_mouse_motion(self, x, y, dx, dy):
		pass
		
	def on_mouse_press(self, x, y, button, modifiers):
		pass
		#pyglet.window.mouse.LEFT
		#pyglet.window.mouse.MIDDLE
		#pyglet.window.mouse.RIGHT

	def on_mouse_release(self, x, y, button, modifiers):
		pass

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		pass
	
	def on_mouse_enter(self, x, y, buttons, modifiers):
		pass

	def on_mouse_leave(self, x, y, buttons, modifiers):
		pass
	
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		pass
	
	def on_resize(self, width, height):
        pass
			
if __name__ == "__main__":
	size = (800,600)
	main = Main(size, window)

	player = Player("img/char_sheet.png")
	main.addObject(player, (100,100))

	block = Block("img/block.png")
	main.addObject(block, (400,400))
	
	main.run()
