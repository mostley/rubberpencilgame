from pyglet.window import key

Settings = {
	"MapPath": "maps/",
	"PenetrationForce": 2.0,
	"Keyboard_Camera_Center": key.C,
	"Keyboard_Player_Attack": key.X,
	"Keyboard_Player_Left": key.LEFT,
	"Keyboard_Player_Right": key.RIGHT,
	"Keyboard_Player_Up": key.UP,
	"Keyboard_Player_Down": key.DOWN,
}

try:
	file = open("rpg.conf", 'r')

	for line in file:
		data = line.split("=")
		Settings[data[0].strip()] = eval(data[1].strip())
except:
	print "Error parsing ConfigFile"
