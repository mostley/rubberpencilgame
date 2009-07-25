import rabbyt
from pyglet import font

class SpriteText(rabbyt.BaseSprite):
	mapSpaceX = 0
	mapSpaceY = 0
	z = rabbyt.anim_slot()
	xyz = rabbyt.swizzle('x', 'y', 'z')
	
	def __init__(self, ft, text, x, y, *args, **kwargs):
		rabbyt.BaseSprite.__init__(self, *args, **kwargs)
		self._text = font.Text(ft, text)
		self.mapSpaceX = x
		self.mapSpaceY = y
	
	def set_text(self, text):
		self._text.text = text
	
	def render_after_transform(self):
		self._text.z = self.z
		self._text.color = self.rgba
		self._text.draw()
