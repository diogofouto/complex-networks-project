import networkx as nx
from copy import deepcopy
from .arena import Arena
from .player import Player

class Simulation:
    def __init__(self, topology=None, players_info=(), num_rounds=1, num_timesteps=100):
        # Check for main arguments
        assert topology is not None, TypeError('__init__ missing \'topology\'')
        assert len(states) != 0, TypeError('__init__ missing \'states\'')

        self.G = topology
        self.players_info = players_info
        self.num_rounds = num_rounds
        self.num_timesteps = num_timesteps

        # Statistics
        self.opinions = []      # A list of dictionaries for each timestep, with opinions for each id
        self.prejudices = []    # A list of dictionaries for each timestep, with prejudice for each pair
                                # That is, the table P for AA, AB, BA and BB

    def run(self):
        print('Starting simulation...')
        for i in range(self.num_rounds):
            print('Round: {}'.format(i))
            self.run_round(i)
        print('Simulation completed')

    def run_round(self, round_no=0):
        self.arena = Arena(self.G.copy())

        print('Creating players...')
        for i in self.arena.G.nodes():
            self.arena.G.node[i]['player'] = Player(arena=self.arena, player_id=i, player_info=deepcopy(self.players_info[i]))
        print('Players created')

        # Run round
        self.arena.run(num_timesteps=self.num_timesteps)