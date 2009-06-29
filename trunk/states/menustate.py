import pygame
from statemachine import State

class MenuState(State):
	font = None
	
	def __init__(self, statemachine):
		State.__init__(self, statemachine)
		
		self.font = pygame.font.Font(None, 12)
	
	def draw(self, visualizer, dt):
		State.draw(self, visualizer, dt)
		
		x = self.font.render("Start", True, (255,0,0))
		#visualizer.screen.blit(x, (0,0))
		
	
	def update(self, dt):
		State.update(self, dt)
	
