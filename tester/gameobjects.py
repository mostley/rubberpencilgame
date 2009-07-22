import rabbyt, pyglet
from pyglet.window import key
from math import *

from enums import *
from settings import Settings

class GameObject(rabbyt.Sprite):
	sprite = None
	showaabb = True
	
	def get_left(self): return self.sprite.left
	def set_left(self, val): self.sprite.left = val
	left = property(get_left, set_left)
	
	def get_right(self): return self.sprite.right
	def set_right(self, val): self.sprite.right = val
	right = property(get_right, set_right)
	
	def get_top(self): return self.sprite.top
	def set_top(self, val): self.sprite.top = val
	top = property(get_top, set_top)
	
	def get_bottom(self): return self.sprite.bottom
	def set_bottom(self, val): self.sprite.bottom = val
	bottom = property(get_bottom, set_bottom)
	
	def get_x(self): return self.sprite.x
	def set_x(self, val): self.sprite.x = val
	x = property(get_x, set_x)
	
	def get_y(self): return self.sprite.y
	def set_y(self, val): self.sprite.y = val
	y = property(get_y, set_y)
	
	def get_w(self): return self.sprite.shape.width
	def set_w(self, val): self.sprite.shape.width = val
	w = width = property(get_w, set_w)
	staticWidth = 0
	
	def get_h(self): return self.sprite.shape.height
	def set_h(self, val): self.sprite.shape.height = val
	h = height = property(get_h, set_h)
	staticHeight = 0
	
	def __init__(self, texture):
		print "Loading Object with Texture: ", texture
		self.sprite = rabbyt.Sprite(texture)
		self.staticWidth = self.sprite.shape.width = 50.0
		self.staticHeight = self.sprite.shape.height = 50.0
		
		self.sprite.parent = self
	
	def render(self, dt):
		self.sprite.render()
		
		if self.showaabb:
			#print repr(self)
			w = int(self.sprite.shape.width)
			h = int(self.sprite.shape.height)
			x = int(self.sprite.x - self.sprite.shape.width/2)
			y = int(self.sprite.y - self.sprite.shape.height/2)
			
			pyglet.gl.glColor3f(0.0, 0.0, 0.0) # set color to black
			lines = (x, y, 
					 x, y + h,
					 x + w, y + h,
					 x + w, y,
					 x, y,
					 x + w, y + h,
					 x + w, y,
					 x, y + h)
			pyglet.graphics.draw(len(lines)/2, pyglet.gl.GL_LINE_STRIP, ('v2i', lines))
	
	def getSprites(self): return [self.sprite]
	def setPosition(self, pos): (self.sprite.x, self.sprite.y) = pos
	def getRect(self): return (self.sprite.x, self.sprite.y, self.width, self.height)
	def getIntegerRect(self): return (int(self.sprite.x), int(self.sprite.y), int(self.width), int(self.height))
	def __repr__(self): return "x: %d y: %d w: %d h: %d" % (self.sprite.x, self.sprite.y, self.width, self.height)
	
	def moveAwayFrom(self, obj, dt=0.1):
		x = float(obj.x) - float(self.x)
		y = float(obj.y) - float(self.y)
		l = float(sqrt(x**2.0 + y**2.0))
		
		if x != 0:
			x /= l
		if y != 0:
			y /= l
		
		self.x -= x * Settings["PenetrationForce"]
		self.y -= y * Settings["PenetrationForce"]

class Block(GameObject):
	def __init__(self, texture):
		GameObject.__init__(self, texture)
	
	def render(self, dt):
		GameObject.render(self, dt)

class Charactor(GameObject):
	lastFrameShift = 0
	frameCount = 12.0
	speed = 100
	nextMovementDirection = MovementDirection.NoWhere
	frozen = False
	
	def __init__(self, texture):
		GameObject.__init__(self, texture)
		self.sprite.tex_shape.width /= self.frameCount
		self.sprite.tex_shape.left = 0
	
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
			self.sprite.shape = [self.w/2, self.h/2, -self.w/2, -self.h/2]
		elif self.isMovingRight():
			#charactor.texture = "img/char_right.png"
			self.sprite.shape = [-self.w/2, self.h/2, self.w/2, -self.h/2]
		#elif self.isMovingUp():
			#charactor.texture = "img/char_up.png"
		#elif self.isMovingDown():
			#charactor.texture = "img/char_down.png"
		
		if not self.isMovingNoWhere():
			self.lastFrameShift += dt
			
			if self.lastFrameShift > 0.05:
				self.lastFrameShift = 0
				
				self.sprite.tex_shape.left += self.sprite.tex_shape.width
				if self.sprite.tex_shape.left >= self.sprite.tex_shape.width * self.frameCount:
					self.sprite.tex_shape.left = self.sprite.tex_shape.width
	
	def handleMovement(self, dt):
		speed = self.speed
		
		if (self.isMovingLeft() or self.isMovingRight()) and (self.isMovingUp() or self.isMovingDown()):
			speed *= 0.7
		
		if self.isMovingLeft():
			self.x -= speed * dt
		elif self.isMovingRight():
			self.x += speed * dt
		
		if self.isMovingUp():
			self.y += speed * dt
		elif self.isMovingDown():
			self.y -= speed * dt
		

class Player(Charactor):
	def __init__(self, texture):
		Charactor.__init__(self, texture)
	
	def determineDirection(self, keyboardHandler):
		self.nextMovementDirection = MovementDirection.NoWhere
		
		if keyboardHandler[key.LEFT]:
			self.nextMovementDirection |= MovementDirection.Left
		if keyboardHandler[key.RIGHT]:
			self.nextMovementDirection |= MovementDirection.Right
		if keyboardHandler[key.UP]:
			self.nextMovementDirection |= MovementDirection.Up
		if keyboardHandler[key.DOWN]:
			self.nextMovementDirection |= MovementDirection.Down
		

class Enemy(Charactor):
	def __init__(self, texture):
		Charactor.__init__(self, texture)
	
	def determineDirection(self):
		pass
