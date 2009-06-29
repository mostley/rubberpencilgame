
class State:
	statemachine = None
	
	def __init__(self,statemachine):
		self.statemachine = statemachine
	
	def draw(self, visualizer, dt):
		pass
		
	def update(self, dt):
		pass

class Statemachine:
	states = []
	main = None
	
	def __init__(self, main):
		self.main = main
	
	def append(self, state):
		self.states.append(state)
	
	def draw(self, visualizer, dt):
		for state in self.states:
			state.draw(visualizer, dt)
	
	def update(self, dt):
		for state in self.states:
			state.update(dt)
