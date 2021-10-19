import os
import random
from copy import deepcopy
from collections import OrderedDict
from .environment import Environment
from . import utils
import numpy.random as rnd


class Player(object):

    def __init__(self, arena=None, player_id=None, tag=None):
        # Check for environment
        assert environment is not None, TypeError('There has to be an environment for the game to commence.')

        # Newborn player parameters
        self.id = player_id
        self.tag = tag
        # Prisoner's Dilemma
        # self.strategy = rnd.choice(["C", "D"])
        self.wealth = 0.5
        self.payoff = payoff

        # Global parameters
        self.global_topology = arena.G

        # Welcome player to environment
        self.env = arena
        self.action = self.env.process(self.run())

    def run(self):
        while True:
            self.play()

    # Prisoner's Dilemma
    def play(self):
        raise NotImplementedError(self)

        #g = updatePayoff()
        #g = updateStrategy()

    def get_all_nodes(self):
        return self.global_topology.nodes()

    def get_players(self, tag_id=None, limit_neighbors=False):
        if limit_neighbors:
            players = self.global_topology.neighbors(self.id)
        else:
            players = self.get_all_nodes()

        if tag_id is None:
            return [self.global_topology.node[_]['player'] for _ in players]  # return all regardless of tag
        else:
            return [self.global_topology.node[_]['player'] for _ in players
                    if self.global_topology.node[_]['player'].tag['id'] == tag_id]

    def get_all_players(self, tag_id=None):
        return self.get_players(tag_id=tag_id, limit_neighbors=False)

    def get_neighboring_players(self, tag_id=None):
        return self.get_players(tag_id=tag_id, limit_neighbors=True)

    def get_neighboring_nodes(self):
        return self.global_topology.neighbors(self.id)

    def get_player(self, player_id):
        return self.global_topology.node[player_id]['player']

    def add_node(self, player_type=None, tag=None):
        player_id = int(len(self.global_topology.nodes()))
        player = player_type(self.env, player_id=player_id, tag=tag)
        self.global_topology.add_node(player_id, {'player': player})
        return player_id


    def add_edge(self, player_id1, player_id2, edge_attr_dict=None, *edge_attrs):
        if player_id1 in self.global_topology.nodes(data=False):
            if player_id2 in self.global_topology.nodes(data=False):
                self.global_topology.add_edge(player_id1, player_id2, edge_attr_dict=edge_attr_dict, *edge_attrs)
            else:
                raise ValueError('\'player_id2\'[{}] not in list of existing players in the network'.format(player_id2))
        else:
            raise ValueError('\'player_id1\'[{}] not in list of existing players in the network'.format(player_id1))

    def remove_node(self, player_id):
        self.global_topology.remove_node(player_id)

    def die(self):
        self.remove_node(self.id)