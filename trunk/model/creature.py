from avatar import Avatar

class Creature:
	avatar = Avatar()
	
	name = ""
	description = ""
	
	stats = {}
	
	def __init__(self):
		stats = {
			hitpoints: 0,
			dexterity_range: 0,
			dexterity_melee: 0,
			strength: 0,
			toughness: 0,
			speed: 0,
			armor: 0
		}
