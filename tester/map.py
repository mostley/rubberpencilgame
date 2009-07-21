from settings import Settings
from gameobjects import *

class Map:
	tiledata = {}
	name = ""
	size = (0,0)
	tilesize = (0,0)
	
	def getWidth(self): return self.size[0]
	w = width = property(getWidth)
	def getHeight(self): return self.size[1]
	h = height = property(getHeight)
	
	
	def __init__(self, name):
		self.name = name
	
	def getTile(self, x, y):
		""" it's an array you will get! """
		result = None
		
		if self.tiledata.has_key(x) and self.tiledata[x].has_key(y):
			result = self.tiledata[x][y]
		
		return result
	
	def update(self, dt): pass
	def draw(self, dt): pass
	
	def save(self):
		pass # todo?
	
	def load(self):
		result = True
		filename = self.getFileName()
		
		file = None
		try:
			file = open(filename, "r")
		except:
			print "no such file '%s'" % filename
			result = False
			
		if file:
			lineNumber = 0
			
			for line in file:
				lineNumber += 1
				line = MapLine(self, line, lineNumber)
				
				if not line.empty():
					if line.isCommentLine():
						continue
					if line.isConfigLine():
						result = line.parseConfig()
					else:
						result = line.parseData()
					
					if not result: break
			
			file.close()
		else:
			print "no Data in Map file '%s'" % filename
			result = False
			
		
		return result
	
	def getFileName(self): return Settings["MapPath"] + self.name + ".map"

class MapLine:
	text = ""
	number = 0
	data = None
	parameters = None
	map = None
	
	def __init__(self, map, text, number):
		self.map = map
		self.text = text.strip()
		self.data = text.split(" ")
		self.number = number
	
	def empty(self): return len(self.data) <= 0 or len(self.text) <= 0
	def isConfigLine(self): return self.text[0] == '+'
	def isCommentLine(self): return self.text[0] == '#'
	
	def parseIntegerTuple(self, inputA, inputB):
		a = None
		b = None
		
		try:
			a = int(inputA)
			b = int(inputB)
		except:
			self.logParseError("Width or Height parameter is not numerical")
			result = False
		
		return a, b
	
	def parseConfig(self):
		result = True
		
		self.data = self.data[1:] # remove '+'
		type = self.data[0].strip().lower()
		
		if type == "size":
			if len(self.data) >= 3:
				w, h = self.parseIntegerTuple(self.data[1], self.data[2])
				if w and h:
					self.map.size = (w, h)
			else:
				self.logParseError("Wrong Number of Arguments. Use format: '+ SIZE Width Height'")
				result = False
		elif type == "tilesize":
			if len(self.data) >= 3:
				w, h = self.parseIntegerTuple(self.data[1], self.data[2])
				if w and h:
					self.map.tilesize = (w, h)
			else:
				self.logParseError("Wrong Number of Arguments. Use format: '+ TILESIZE Width Height'")
				result = False
		
		return result
	
	def parseData(self):
		result = True
		
		if len(self.data) >= 5:
			tile = MapTile(self.map)
			tile.x = float(self.data[0])
			tile.y = float(self.data[1])
			tile.w = float(self.data[2])
			tile.h = float(self.data[3])
			tile.type = self.data[4].lower()
			tile.setParameters(self.data[5:])
			
			if not self.map.tiledata.has_key(tile.x):
				self.map.tiledata[tile.x] = {}
			if not self.map.tiledata[tile.x].has_key(tile.y):
				self.map.tiledata[tile.x][tile.y] = []
			
			self.map.tiledata[tile.x][tile.y].append(tile)
		else:
			self.logParseError("Wrong Number of Arguments. Use format: 'X Y Width Height TYPE Parameters'")
			result = False
		
		return result
	
	def logParseError(self, error):
		print "Error on Line %d of Mapfile '%s': '%s'" % (self.number, self.getFileName(), error)

class MapTile:
	x = 0
	y = 0
	w = 1
	h = 1
	type = None
	map = None
	
	def getParameters(self): return self.params
	def setParameters(self, params): self.params = params
	params = property(getParameters, setParameters)
	
	def __init__(self, map):
		self.map = map
	
	def serialize(self):
		return ""
	
	def getSprite(self):
		result = None
		if self.type == "block":
			texture = None
			if self.params:
				texture = self.params[0].strip()
			result = Block(texture)
			result.setPosition((self.x, self.y))
			result.width, result.height = self.w, self.h
		else:
			pass
			#todo: implement rest
		
		return result
