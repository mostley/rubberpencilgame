from settings import Settings
from gameobjects import *

class Map:
	tiledata = {}
	name = ""
	size = (0,0)
	tilesize = (0,0)
	playerPos = (0,0)
	playerStartPos = (0,0)
	playerEnterSpeed = 1
	enemies = []
	enemyRoutes = []
	main = None
	
	def getWidth(self): return self.size[0]
	w = width = property(getWidth)
	def getHeight(self): return self.size[1]
	h = height = property(getHeight)
	
	
	def __init__(self, name, main):
		self.name = name
		self.main = main
	
	def getNearestRoutPoint(self, obj):
		result = None
		resultdist = 99999
		for route in self.enemyRoutes:
			for point in route:
				if result == None:
					result = point
				else:
					dist = obj.getDistance(point)
					if dist < resultdist:
						result = point
						resultdist = dist
		return result
	
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
				line = MapLine(self, line.replace("  ", " ").strip(), lineNumber)
				
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
	
	def parseInteger(self, input):
		a = None
		
		try:
			a = int(input)
		except:
			self.logParseError("parameter is not numerical")
			result = False
		
		return a
	
	def parseFloat(self, input):
		a = None
		
		try:
			a = float(input)
		except:
			self.logParseError("parameter is not numerical")
			result = False
		
		return a
	
	def parseIntegerTuple(self, inputA, inputB):
		a = self.parseInteger(inputA)
		b = self.parseInteger(inputB)
		
		return a, b
	
	def parseConfig(self):
		result = True
		
		self.data = self.data[1:] # remove '+'
		type = self.data[0].strip().lower()
		
		if type == "size":
			if len(self.data) >= 3:
				w, h = self.parseIntegerTuple(self.data[1], self.data[2])
				if w != None and h != None:
					self.map.size = (w, h)
			else:
				self.logParseError("Wrong Number of Arguments. Use format: '+ SIZE Width Height'")
				result = False
				
		elif type == "tilesize":
			if len(self.data) >= 3:
				w, h = self.parseIntegerTuple(self.data[1], self.data[2])
				if w != None and h != None:
					self.map.tilesize = (w, h)
			else:
				self.logParseError("Wrong Number of Arguments. Use format: '+ TILESIZE Width Height'")
				result = False
				
		elif type == "playerpos":
			if len(self.data) >= 6:
				x, y = self.parseIntegerTuple(self.data[1], self.data[2])
				sx, sy = self.parseIntegerTuple(self.data[3], self.data[4])
				speed = self.parseFloat(self.data[5])
				if x != None and y != None and sx != None and sy != None and speed != None:
					self.map.playerPos = (x, y)
					self.map.playerStartPos = (sx, sy)
					self.map.playerEnterSpeed = speed
			else:
				self.logParseError("Wrong Number of Arguments. Use format: '+ PLAYERPOS X Y StartX StartY'")
				result = False
				
		elif type == "enemy":
			if len(self.data) >= 5:
				x, y = self.parseIntegerTuple(self.data[1], self.data[2])
				level = self.parseInteger(self.data[3])
				if x != None and y != None and level != None:
					enemy = Enemy(self.data[4], level, self.map.main)
					enemy.setPosition((x,y))
					print enemy
					self.map.enemies.append(enemy)
			else:
				self.logParseError("Wrong Number of Arguments. Use format: '+ ENEMY X Y Level Texture'")
				result = False
				
		elif type == "enemyroute":
			if len(self.data) >= 1:
				route = []
				for tuple in self.data[1:]:
					tuple = tuple.split(":")
					x, y = self.parseIntegerTuple(tuple[0], tuple[1])
					if x != None and y != None:
						route.append(RoutePoint(x,y))
				
				for i in range(len(route)):
					if i < len(route)-1:
						route[i].nextPoint = route[i+1]
					if i > 0:
						route[i].previousPoint = route[i-1]
				route[0].previousPoint = route[len(route)-1]
				route[len(route)-1].nextPoint = route[0]
				
				self.map.enemyRoutes.append(route)
			else:
				self.logParseError("Wrong Number of Arguments. Use format: '+ ENEMYROUTE X:Y X:Y X:Y ...'")
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
		print "Error on Line %d of Mapfile '%s': '%s'" % (self.number, self.map.getFileName(), error)

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
		
		elif self.type == "background":
			pass
		
		elif self.type == "action":
			pass
		
		#todo: implement rest
		
		return result

class RoutePoint:
	x,y = 0,0
	bounding_radius = 0
	nextPoint = None
	previousPoint = None
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
