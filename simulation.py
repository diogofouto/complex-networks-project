import networkx as nx
from copy import deepcopy
from arena import Arena
from player import Player



class Simulation:
	def __init__(self, topology=None, num_attempts=1, num_timesteps=100):
		# Check for main arguments
		assert topology is not None, TypeError('__init__ missing \'topology\'')

		self.G = topology
		self.num_attempts = num_attempts
		self.num_timesteps = num_timesteps

		# Statistics
		self.opinions = []      # A list of dictionaries for each timestep, with opinions for each id
		self.prejudices = []    # A list of dictionaries for each timestep, with prejudice for each pair
								# That is, the table P for AA, AB, BA and BB


	def run(self):
		for i in range(self.num_attempts):
			print('Starting simulation attempt {}...'.format(i))
			self.run_attempt(i)
			print('Simulation attempt {} completed successfully!'.format(i))


	def run_attempt(self, attempt_no=0):
		# Copy and save arena
		self.arena = Arena(self.G.copy())
		Player.arena = self.arena

		print('Creating players...')
		for i in self.arena.G.nodes():
			self.arena.G.nodes[i]['player'] = Player(player_id=i)
		print('Players created!')

		# Run attempt for num_timesteps
		opinions, biases = self.arena.run(num_timesteps=self.num_timesteps)

		# Draw Visualization
		nx.draw(self.arena.G)

		# Show statistics
		print("OPINIONS:")
		print(opinions, '\n')

		print("BIASES:")
		print(biases, '\n')




