
class Map:
	tiledata = {}
	codedata = {}
	imagedata = []
	engine = None
	name = ""
	tilesize = (0,0)
	
	def __init__(self, engine, name):
		self.engine = engine
		self.name = name
	
	def save(self):
		pass #todo pickle dump it
	
	def load(self, visualizer):
		#TODO load mapdata from file
		
		self.tiledata = {
			#0x01:('player',tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
			#0x02:('player',tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
			#0x20:('player',tile_coin,None),
			#0x30:('player',tile_fire,None),
		}
		self.codedata = {
			#1:(self.player_new,None),
			#2:(enemy_new,{'move':enemy_move_line}),
			#3:(enemy_new,{'move':enemy_move_sine}),
			#4:(enemy_new,{'move':enemy_move_circle}),
		}
		self.imagedata = [
			#('player','player.tga',(4,4,24,24)),
			#('enemy','enemy.tga',(4,4,24,24)),
			#('shot','shot.tga',(1,2,6,4)),
		]
		self.tilesize = (32,32)
		
		
		(engine.view.w, engine.view.h) = visualizer.size
		self.engine.screen = visualizer.screen
		self.frame = 0
		self.engine.quit = 0
		
		self.engine.tga_load_tiles('data/levels/'+self.name+'/tiles.tga', self.tilesize, self.tiledata)
		self.engine.tga_load_level('data/levels/'+self.name+'/level.tga', 1)
		
		(x,y) = self.tilesize
		w = (len(self.engine.tlayer[0])-2) * x
		h = (len(self.engine.tlayer)-2) * y
		self.engine.bounds = pygame.Rect(x,y,w,h)
		self.engine.load_images(self.imagedata)
		self.engine.run_codes(self.codedata,(0,0,25,17))
		
		self.engine.font = pygame.font.SysFont('helvetica',16)
		
		self.engine.paint(self.engine.screen)
		pygame.display.flip()
	
