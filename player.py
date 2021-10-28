import networkx as nx
import numpy as np


class Player:

	# ---------------------- STATIC VARIABLES -----------------------

	arena = None # where all players reside
	global_bias = [[0.5, 0.5], [0.5, 0.5]] # bias between tags


	# ----------------------- MAIN FUNCTIONS ------------------------

	def __init__(self, player_id=None):
		assert player_id is not None, TypeError('No player_id given.')

		# Neutral player
		self.id = player_id
		self.tag = 0.5
		self.bias = Player.global_bias
		self.payoff = 0

		# For SimPy
		self.env = Player.arena
		self.env.process(self.run())

	def run(self):
		while True:
			self.play_with_neighbors()
			yield self.env.timeout(1) # each interaction takes 1 timestep


	# --------------------- PRISONER'S DILEMMA ----------------------
	
	def play_with_neighbors(self):
		for player in self.get_players(just_neighbors=True): # For each neighbor
			
			# Choose own's tactic
			own_cooperate_prob = self.bias[round(self.tag)][round(player.tag)]
			own_choice = np.random.choice(a=['C', 'D'], p=[own_cooperate_prob, 1-own_cooperate_prob])
			
			# Get other player's tactic
			other_cooperate_prob = player.bias[round(player.tag)][round(self.tag)]
			other_choice = np.random.choice(a=['C', 'D'], p=[other_cooperate_prob, 1-other_cooperate_prob])

			# Record previous payoffs
			own_previous_payoff = self.payoff
			other_previous_payoff = player.payoff

			# Play
			if own_choice == other_choice:
				if own_choice == 'C':
					self.payoff += 1
					player.payoff += 1
				else:
					self.payoff += 2
					player.payoff += 2
			else:
				if own_choice == 'D':
					player.payoff += 3
				else:
					self.payoff += 3

			# Update own bias
			if self.payoff > own_previous_payoff:
				pass
			else:
				pass

			# Update other player's bias
			if player.payoff > other_previous_payoff:
				pass
			else:
				pass

	def update_bias(self, game_score=None, other_player_tag=None):
		pass


	# ---------------------- HELPER FUNCTIONS -----------------------
	
	def get_players(self, tag=None, just_neighbors=False):
		if just_neighbors:  
			nodes = Player.arena.G.neighbors(self.id)
		else:
			nodes = Player.arena.G.nodes()

		if tag is None:
			return [Player.arena.G.nodes[n]['player'] for n in nodes]
		else:
			return [Player.arena.G.nodes[n]['player'] for n in nodes
					if Player.arena.G.nodes[n]['player'].tag['id'] == tag]