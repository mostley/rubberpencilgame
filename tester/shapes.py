from pyglet.gl import *

class Shape(object):
	primitives = []
	
	def __init__(self, verts, colors, position, angle=0):
		self.verts = verts
		self.colors = colors
		self.x, self.y = position
		self.angle = angle
	
	def render(self):
		for prim in self.primitives:
			draw( len(primitive.verts),
				  primitive.primtype,
				  ('v2f', shape.verts),
				  ('c3B', shape.colors), )

def renderShapeList(shapes):
	for shape in shapes:
		glPushMatrix()
		glTranslatef(shape.x, shape.y, 0)
		glRotatef(shape.angle * rad2deg, 0, 0, 1)
		draw(3, GL_TRIANGLES,
			('v2f', shape.verts),
			('c3B', shape.colors),
		glPopMatrix()

class Primitive(object):
	def __init__(self, verts, color, primtype):
		self.verts = verts
		self.color = color
		self.primitive = primtype # eg. GL_TRIANGLES
	

