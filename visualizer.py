import pygame,rabbyt

class Visualizer:
	screen = None
	size = (640,480)
	main = None
	
	def __init__(self, main):
		self.main = main
		pygame.init()
		self.screen = pygame.display.set_mode(self.size, pygame.OPENGL | pygame.DOUBLEBUF)
		rabbyt.set_viewport(self.size)
		rabbyt.set_default_attribs()
		
		pygame.font.init();
	
	def draw(self, statemachine, dt):
		rabbyt.clear()
		
		statemachine.draw(self, dt)
		
		pygame.display.flip()
