from pyglet.gl import *
	
	#def focus(self, win_width, win_height):
		#glMatrixMode(GL_PROJECTION)
		#glLoadIdentity()
		#aspect = win_width / win_height
		#gluOrtho2D(-self.scale * aspect, # left
				   #+self.scale * aspect, # right
				   #-self.scale,          # bottom
				   #+self.scale)          # top
		
		## Set modelview matrix to move, scale & rotate
		#glMatrixMode(GL_MODELVIEW)
		#glLoadIdentity()
		#gluLookAt(self.x, self.y, +1.0, # camera  x,y,z
				  #self.x, self.y, -1.0, # look at x,y,z
				  #sin(self.angle), cos(self.angle), 0.0)

class Camera(object):
	mode = 1
	x,y,z = 0,0,512
	rx,ry,rz = 30,-45,0
	w,h = 640,480
	far = 8192
	fov = 60
	zoomV = 0
	zoomSpeed = 20
	minZoom = 10
	maxZoom = 100
	zoomFriction = 0.9
	panSpeed = 70
	
	def __init__(self, startposition, scale=1, angle=0):
		self.startposition = startposition
		self.reset()
		   
	def view(self,width,height):
		self.w,self.h = width,height
		glViewport(0, 0, width, height)
		print "Viewport " + str(width) + "x" + str(height)
		if self.mode == 2: self.isometric()
		elif self.mode == 3: self.perspective()
		else: self.default()
		   
	def default(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, self.w, 0, self.h, -1, 1)
		glMatrixMode(GL_MODELVIEW)
	   
	def isometric(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-self.w/2.,self.w/2.,-self.h/2.,self.h/2.,0,self.far)
		glMatrixMode(GL_MODELVIEW)
	   
	def perspective(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(self.fov, float(self.w)/self.h, 0.1, self.far)
		glMatrixMode(GL_MODELVIEW)
	   
	def key(self, symbol, modifiers):
		if symbol == key.F1:
			self.mode = 1
			self.default()
			print "Projection: Pyglet default"
		elif symbol == key.F2:
			print "Projection: 3D Isometric"
			self.mode = 2
			self.isometric()
		elif symbol == key.F3:
			print "Projection: 3D Perspective"
			self.mode = 3
			self.perspective()
		elif self.mode == 3 and symbol == key.NUM_SUBTRACT:
			self.fov -= 1
			self.perspective()
		elif self.mode == 3 and symbol == key.NUM_ADD:
			self.fov += 1
			self.perspective()
		else: print "KEY " + key.symbol_string(symbol)
	
	def reset(self):
		self.x, self.y = self.startposition
		self.mode = 2
		self.rx,self.ry,self.rz = 0,0,0
		self.fov = 60
	   
	def drag(self, x, y, dx, dy, button, modifiers):
		if button == 1:
			f = self.fov/self.panSpeed
			#print self.fov, f
			self.x -= dx * f
			self.y -= dy * f
		elif button == 4:
			self.ry += dx/4.
			self.rx -= dy/4.
		#print self.rx,self.ry,self.rz,self.x,self.y,self.z
	
	def update(self, dt):
		#print self.zoomV * dt
		if self.fov > self.minZoom and self.fov < self.maxZoom:
			self.fov += self.zoomV * dt
			self.perspective()
		else:
			self.zoomV = 0
			if self.fov >= self.maxZoom: self.fov = self.maxZoom - 1
			elif self.fov <= self.minZoom: self.fov = self.minZoom + 1
		
		self.zoomV *= self.zoomFriction
		#print self.fov,self.zoomV
	
	def zoomOut(self):
		self.zoomV += self.zoomSpeed
	
	def zoomIn(self):
		self.zoomV -= self.zoomSpeed
	
	def toWorldSpace(self, x, y, z): return x + self.x - 320, y + self.y - 240, z + (self.fov - 60)*6.6
	
	def focusOn(self, obj):
		x,y,z = self.toWorldSpace(obj.x, obj.y, 0)
		#self.x, self.y, self.z = x,y,z
		print self.x, self.y, "-", x, y
		self.x, self.y = x, y
		print self.x, self.y, self.z
	
	def apply(self):
		glLoadIdentity()
		if self.mode == 1: return
		glTranslatef(-self.x,-self.y,-self.z)
		glRotatef(self.rx,1,0,0)
		glRotatef(self.ry,0,1,0)
		glRotatef(self.rz,0,0,1)
