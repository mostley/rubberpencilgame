import rabbyt, pyglet
from enums import *

class GameObject(rabbyt.Sprite):
	sprite = None
	showaabb = True
	width = 50
	height = 50
	
	def __init__(self, texture):
		self.sprite = rabbyt.Sprite(texture)
		self.sprite.shape = [-self.width, -self.height, self.width, self.height]
	
	def render(self, dt):
		self.sprite.render()
		if self.showaabb:
			#print repr(self)
			x = int(self.sprite.x)
			y = int(self.sprite.y)
			w = int(self.width)
			h = int(self.height)
			
			pyglet.gl.glColor3f(0.0, 0.0, 0.0) # set color to black
			lines = (x, y, 
					 x, y + h,
					 x, y + h,
					 x + w, y + h,
					 x + w, y + h,
					 x + w, y,
					 x + w, y,
					 x, y)
			pyglet.graphics.draw(len(lines)/2, pyglet.gl.GL_LINES, ('v2i', lines))
	
	def getSprites(self): return [self.sprite]
	def setPosition(self, pos): (self.sprite.x, self.sprite.y) = pos
	def getRect(self): return (self.sprite.x, self.sprite.y, self.width, self.height)
	def getIntegerRect(self): return (int(self.sprite.x), int(self.sprite.y), int(self.width), int(self.height))
	def __repr__(self): return "x: %d y: %d w: %d h: %d" % (self.sprite.x, self.sprite.y, self.width, self.height)

class Block(GameObject):
	def __init__(self, texture):
		GameObject.__init__(self, texture)
	
	def render(self, dt):
		GameObject.render(self, dt)

class Charactor(GameObject):
	lastFrameShift = 0
	spriteWidthFraction = 1.0/12.0
	speed = 20
	stepsize = 5.0
	nextMovementDirection = MovementDirection.NoWhere
	frozen = False
	
	def __init__(self, texture):
		GameObject.__init__(self, texture)
		self.sprite.tex_shape = [0,1,self.spriteWidthFraction,0]
	
	def update(self, dt):
		self.animate(dt)
		
		if not self.frozen:
			self.handleMovement(dt)
		else:
			self.frozen = False
	
	def isMovingNoWhere(self): return self.nextMovementDirection == MovementDirection.NoWhere
	def isMovingLeft(self): return (self.nextMovementDirection & MovementDirection.Left) == MovementDirection.Left
	def isMovingRight(self): return (self.nextMovementDirection & MovementDirection.Right) == MovementDirection.Right
	def isMovingUp(self): return (self.nextMovementDirection & MovementDirection.Up) == MovementDirection.Up
	def isMovingDown(self): return (self.nextMovementDirection & MovementDirection.Down) == MovementDirection.Down
	
	def animate(self, dt):
		if self.isMovingLeft():
			#charactor.texture = "img/char_left.png"
			self.sprite.shape = [self.width, -self.height, -self.width, self.height]
		elif self.isMovingRight():
			#charactor.texture = "img/char_right.png"
			self.sprite.shape = [-self.width, -self.height, self.width, self.height]
		#elif self.isMovingUp():
			#charactor.texture = "img/char_up.png"
		#elif self.isMovingDown():
			#charactor.texture = "img/char_down.png"
		
		if not self.isMovingNoWhere():
			if dt - self.lastFrameShift > 30:
				self.lastFrameShift = dt
				self.sprite.u += self.spriteWidthFraction
				if self.sprite.u > 1:
					self.sprite.u = self.spriteWidthFraction
	
	def handleMovement(self, dt):
		if self.isMovingLeft():
			self.sprite.x -= rabbyt.lerp(0,self.stepsize,dt=self.speed)
			
		elif self.isMovingRight():
			self.sprite.x += rabbyt.lerp(0,self.stepsize,dt=self.speed)
			
		if self.isMovingUp():
			self.sprite.y -= rabbyt.lerp(0,self.stepsize,dt=self.speed)
			
		elif self.isMovingDown():
			self.sprite.y += rabbyt.lerp(0,self.stepsize,dt=self.speed)
		

class Player(Charactor):
	def __init__(self, texture):
		Charactor.__init__(self, texture)
	
	def determineDirection(self):
		return None
		#pressed = pygame.key.get_pressed()
		
		self.nextMovementDirection = MovementDirection.NoWhere
		if pressed[K_LEFT]:
			self.nextMovementDirection |= MovementDirection.Left
		if pressed[K_RIGHT]:
			self.nextMovementDirection |= MovementDirection.Right
		if pressed[K_UP]:
			self.nextMovementDirection |= MovementDirection.Up
		if pressed[K_DOWN]:
			self.nextMovementDirection |= MovementDirection.Down
		

class Enemy(Charactor):
	def __init__(self, texture):
		Charactor.__init__(self, texture)
	
	def determineDirection(self):
		pass
