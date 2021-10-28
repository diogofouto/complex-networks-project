import simpy
import networkx as nx
from player import Player

class Arena(simpy.Environment):
	def __init__(self, topology):
		super().__init__(initial_time=0)
		assert isinstance(topology, nx.Graph)
		self.G = topology


	"""
	Run is overriden in order to get the list of the players after each timestep.
	Returns a list of the opinions and a list of global biases for each timestep
	"""
	def run(self, num_timesteps):
		opinions = [] # opinions of each id for each timestep
		global_biases = [] # global biases for each timestep (i.e. the table P for AA, AB, BA and BB)

		for i in range(num_timesteps):
			super().run(until=i+1)

			# store current global bias and all players opinion
			global_biases += Player.global_bias

			current_opinions = []
			for n in self.G.nodes():
				current_opinions.append(self.G.nodes[n]['player'].tag)
			
			opinions.append(current_opinions)
	
		return opinions, global_biases