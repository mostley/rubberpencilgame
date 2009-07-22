#!/usr/bin/python

import os
import sys
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
from map import Map

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""

    return hasattr(sys, "frozen")


def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""

    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))

    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))


class Main(Window):
	objects = []
	sprites = []
	player = None
	textsprite = None
	keyboardHandler = None
	camera = None
	currentMap = None
	
	def __init__(self, size):
		Window.__init__(self, width=size[0], height=size[1])
		
		self.camera = Camera((size[0]/2.0, size[1]/2.0))
		self.on_resize = self.camera.view
		self.on_mouse_drag = self.camera.drag
		
		clock.schedule(rabbyt.add_time)
		clock.set_fps_limit(60)
		
		rabbyt.set_default_attribs()
		rabbyt.data_directory = module_path()
		print "Current Data_Directory:", rabbyt.data_directory
		
		self.keyboardHandler = key.KeyStateHandler()
		self.push_handlers(self.keyboardHandler)
		
		
		ft = font.load('Arial', 24)
		self.textsprite = SpriteText(ft, "Hello World", xy=(320,240))
		self.textsprite.rot = rabbyt.lerp(0,360, dt=5, extend="extrapolate")
		self.textsprite.rgb = rabbyt.lerp((1,0,0), (0,1,0), dt=2, extend="reverse")
		
		self.currentMap = Map("level00")
		if not self.currentMap.load():
			print "Loading Map failed."
			# todo: show mainmenu
		else:
			for x in range(self.currentMap.width):
				for y in range(self.currentMap.height):
					tiles = self.currentMap.getTile(x,y)
					if tiles:
						for tile in tiles:
							obj = tile.getSprite()
							if obj:
								self.addObject(obj, (x,y))
		
	
	def addObject(self, obj, pos):
		print obj,pos
		obj.setPosition(pos)
		self.objects.append(obj)
		spritelist = obj.getSprites()
		for s in spritelist:
			self.sprites.append(s)
		if isinstance(obj, Player):
			self.player = obj
	
	def updateModel(self, dt):
		self.player.determineDirection(self.keyboardHandler)
		
		collisions2 = rabbyt.collisions.collide_single(self.player.getSprites()[0], self.sprites)
		
		if len(collisions2) > 1:
			for obj in collisions2:
				if obj == self.player: continue
				
				obj.rgb = rabbyt.lerp((1,0,0),(1,1,1), dt=.4)
				self.player.moveAwayFrom(obj)
		
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
		
		self.currentMap.draw(dt)
		
		self.drawGrid()
	
	def run(self):
		while not self.has_exit:
			dt = clock.tick()
			self.dispatch_events()
			
			self.camera.update(dt)
			self.camera.apply()
			
			self.updateModel(dt)
			self.currentMap.update(dt)
			
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

	player = Player(os.path.normcase(module_path()+"/img/char_sheet.png"))
	main.addObject(player, (100,100))

	block = Block(os.path.normcase(module_path()+"/img/block.png"))
	main.addObject(block, (rabbyt.lerp(0,400, endt=15, extend="reverse"),400))
	
	main.run()
