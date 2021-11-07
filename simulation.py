from arena import Arena
from player import Player

class Simulation:
	def __init__(self, topology=None, num_attempts=1, num_timesteps=100):
		# Check for main arguments
		assert topology is not None, TypeError('__init__ missing \'topology\'')

		self.G = topology
		self.num_attempts = num_attempts
		self.num_timesteps = num_timesteps

	def run(self):
		beliefs = []	# A list of dictionaries for each timestep, with beliefs for each id
		biases = []		# A list of dictionaries for each timestep, with prejudice for each pair
						# That is, the table P for AA, AB, BA and BB

		for i in range(self.num_attempts):
			print('Starting simulation attempt {}...'.format(i))
			attempt_beliefs, attempt_biases = self.run_attempt(i)
			print('Simulation attempt {} completed successfully!'.format(i))

			beliefs.append(attempt_beliefs)
			biases.append(attempt_biases)

		return beliefs, biases


	def run_attempt(self):
		def create_players():
			print('Creating players...')

			for i in self.arena.G.nodes():
				self.arena.G.nodes[i]['player'] = Player(arena = self.arena, player_id=i, group_bias=Arena.INIT_GLOBAL_BIAS)

			print('Players created!')

		self.arena = Arena(self.G.copy())
		Player.arena = self.arena

		create_players()

		# Run attempt for num_timesteps
		return self.arena.run(num_timesteps=self.num_timesteps)
