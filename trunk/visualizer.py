import pygame,rabbyt

class Visualizer:
	screen = None
	size = (640,480)
	main = None
	tilevid = None
	tdata = {
		0x01:('player',tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
		0x02:('player',tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
		0x20:('player',tile_coin,None),
		0x30:('player',tile_fire,None),
	}
	
	def __init__(self, main):
		self.main = main
		pygame.init()
		self.screen = pygame.display.set_mode(self.size, pygame.OPENGL | pygame.DOUBLEBUF)
		rabbyt.set_viewport(self.size)
		rabbyt.set_default_attribs()
		
		pygame.font.init();
		
		self.tilevid = tilevid.Tilevid()
		(self.tilevid.view.w,self.tilevid.view.h) = self.size
		self.tilevid.screen = self.screen
		self.frame = 0
		self.tilevid.tga_load_tiles('tiles.tga',self.size,tdata)
	
	def draw(self, statemachine, dt):
		rabbyt.clear()
		
		statemachine.draw(self, dt)
		
		pygame.display.flip()
