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
from settings import Settings

os.environ['PYGLET_SHADOW_WINDOW'] = "0"

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""

    return hasattr(sys, "frozen")

def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""

    if we_are_frozen():
        return os.path.dirname(os.path.abspath(unicode(sys.executable, sys.getfilesystemencoding( ))))

    return os.path.dirname(os.path.abspath(unicode(__file__, sys.getfilesystemencoding( ))))


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
		
		ft = font.load('Arial', 18)
		self.textsprite = SpriteText(ft, "Gold: 0", 0, 500, rgb = (0,0,0))
	
	def unload(self):
		pass
	
	def showMainMenu(self):
		pass
	
	def loadMap(self, mapname):
		self.unload()
		
		self.currentMap = Map(mapname, self)
		if not self.currentMap.load():
			print "Loading Map failed."
			self.showMainMenu()
		else:
			for x in range(self.currentMap.width):
				for y in range(self.currentMap.height):
					tiles = self.currentMap.getTile(x,y)
					if tiles:
						for tile in tiles:
							obj = tile.getSprite()
							if obj:
								self.addObject(obj, (x,y))
			
			self.player.setPosition(self.currentMap.playerStartPos)
			self.player.moveTo(self.currentMap.playerPos, self.currentMap.playerEnterSpeed)
			
			for enemy in self.currentMap.enemies:
				self.addObject(enemy, (enemy.x,enemy.y))
	
	def addObject(self, obj, pos):
		#print obj,pos
		obj.setPosition(pos)
		self.objects.append(obj)
		spritelist = obj.getSprites()
		for s in spritelist:
			self.sprites.append(s)
		if isinstance(obj, Player):
			self.player = obj
	
	def checkCollisions(self, obj, dt):
		collisions = rabbyt.collisions.collide_single(obj.getSprites()[0], self.sprites)
		
		if len(collisions) > 1:
			for other in collisions:
				if other == obj: continue
				
				other.rgb = rabbyt.lerp((1,0,0),(1,1,1), dt=.4) # debug
				obj.collide(other, dt)
		
	def enemyCollision(self, dt):
		for obj in self.objects:
			if isinstance(obj, Enemy):
				self.checkCollisions(obj, dt)
	
	def updateModel(self, dt):
		for obj in self.objects:
			if isinstance(obj, Charactor):
				obj.determineDirection(dt, self.keyboardHandler)
		
		self.checkCollisions(self.player, dt)
		self.enemyCollision(dt)
		
		for obj in self.objects:
			if isinstance(obj, Charactor):
				obj.update(dt)
	
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
		
		self.textsprite.xyz = self.camera.toWorldSpace(self.textsprite.mapSpaceX, self.textsprite.mapSpaceY, 0)
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
	
	def on_key_press(self, symbol, modifiers):
		if symbol == Settings["Keyboard_Camera_Center"]:
			self.camera.reset()
			self.camera.focusOn(self.player)
		elif symbol == Settings["Keyboard_Player_Attack"]:
			self.player.attack()
		else:
			Window.on_key_press(self, symbol, modifiers)
		

if __name__ == "__main__":
	size = (640, 480)
	
	main = Main(size)

	player = Player(os.path.normcase(module_path()+"/img/char_sheet.png"))
	main.addObject(player, (100,100))
	
	#enemy = Enemy(os.path.normcase(module_path()+"/img/enemy_sheet.png"), 0, main)
	#main.addObject(enemy, (500,500))

	block = Block(os.path.normcase(module_path()+"/img/block.png"))
	main.addObject(block, (rabbyt.lerp(0,400, endt=15, extend="reverse"),400))
	
	main.loadMap("level00")
	
	main.run()
