import networkx as nx
from copy import deepcopy
from .arena import Arena
from .player import Player

class Simulation(object):
    def __init__(self, topology=None, states=(), num_rounds=1, num_timesteps=100):
        # Check for main arguments
        assert topology is not None, TypeError('__init__ missing \'topology\'')
        assert len(states) != 0, TypeError('__init__ missing \'states\'')

        self.G = topology
        self.initial_states = states
        self.num_rounds = num_rounds
        self.num_timesteps = num_timesteps

    def run_sim(self):
        print('Starting simulation...')
        for i in range(self.num_trials):
            print('Trial: {}'.format(i))
            self.run_round(i)
        print('Simulation completed')

    def run_round(self, trial_no=0):
        self.arena = Arena(self.G.copy())

        print('Creating players...')
        for i in self.arena.G.nodes():
            self.arena.G.node[i]['player'] = Player(arena=self.arena, player_id=i, state=deepcopy(self.initial_states[i]))
        print('Players created')

        # Run trial
        self.arena.run(num_timesteps=self.num_timesteps)