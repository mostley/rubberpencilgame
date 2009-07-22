import os
import sys
import rabbyt
from pyglet.window import Window
from pyglet import clock
import os.path

os.environ['PYGLET_SHADOW_WINDOW'] = "0"
def we_are_frozen():
	"""Returns whether we are frozen via py2exe.
	This will affect how we find out where we are located."""
	
	return hasattr(sys, "frozen")
def module_path():
	""" This will get us the program's directory,
	even if we are frozen using py2exe"""
	
	if we_are_frozen():
		return os.path.dirname(os.path.abspath(unicode(sys.executable, sys.getfilesystemencoding( ))))
	return os.path.dirname(os.path.abspath(unicode(__file__, sys.getfilesystemencoding( ))))

class Main(Window):
	image = None
	
	def __init__(self, size):
		Window.__init__(self, width=size[0], height=size[1])
		
		clock.schedule(rabbyt.add_time)
		clock.set_fps_limit(60)
		
		rabbyt.set_default_attribs()
		rabbyt.data_directory = module_path()
		print "Current Data_Directory:", rabbyt.data_directory
		
		texture = os.path.normcase(module_path()+"/img/char_sheet.png")
		print "Loading Object with Texture: ", texture
		self.image = rabbyt.Sprite(texture)
					
	def run(self):
		while not self.has_exit:
			self.dispatch_events()
			
			rabbyt.clear((255,255,255))
						
			self.image.render()
			
			self.flip()
	
	
if __name__ == "__main__":
	size = (640, 480)
	main = Main((640, 480))
	main.run()
