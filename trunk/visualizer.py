import pygame,rabbyt
from pgu import tilevid, timer, gui

class Visualizer:
	screen = None
	size = (640,480)
	tilesize = (32,32)
	main = None
	tileengine = None
	app = None

	def __init__(self, main):
		self.main = main
		pygame.init()
		self.screen = pygame.display.set_mode(self.size)#, pygame.OPENGL | pygame.DOUBLEBUF)
		rabbyt.set_viewport(self.size)
		rabbyt.set_default_attribs()
		
		pygame.font.init();
		
		self.app = gui.App()
		self.app.connect(gui.QUIT, self.app.quit, None)
		btn = gui.Button("test")
		self.app.init(btn)
	
	def draw(self, statemachine, dt):
		rabbyt.clear()
		
		statemachine.draw(self, dt)
		
		self.app.paint(self.screen)
		
	
	def quit(self):
		pass
