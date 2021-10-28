import networkx as nx
import numpy as np
from .utils import sigmoid
from .arena import Arena

class Player:

    # ---------------------- STATIC VARIABLES -----------------------

    network = None              # where all players reside
    global_bias = [0.5, 0.5]    # bias towards thinking that a player is cooperator
    FORGETTING_FACTOR = 0.05

    # ----------------------- MAIN FUNCTIONS ------------------------

    def __init__(self, arena=None, player_id=None):
        # Check arguments
        assert arena is not None, TypeError('No arena given.')
        assert player_id is not None, TypeError('No player_id given.')

        # Newborn player params
        self.id = player_id
        self.belief = 0.5
        self.bias = Player.global_bias
        self.round_total_payoff = 0

        # 0 or 1
        self.tag = 0

        # Parameters used to compute the belief

        # sum(1/(t_i + 1)), where i is the id of a node of your tag   
        self.own_tag_inv_payoff = 0
        self.other_tag_inv_payoff = 0

        self.own_tag_cooperators = 0
        self.other_tag_cooperators = 0       

        self.own_tag_count = 0
        self.other_tag_count = 0


        # Initialize network
        Player.network = arena.G

        # For SimPy
        # self.env = arena
        # self.env.process(self.run())


    # --------------------- PRISONER'S DILEMMA ----------------------

    def play_with_neighbour(self, other_player):

        # --------------------- AUXILIARY FUNCTIONS ----------------------

        def choose_tactics():
            return self.choose_tactic(other_player), other_player.choose_tactic(self)

        def compute_payoffs():
            return self.compute_payoff(own_choice, other_choice), other_player.compute_payoff(other_choice, own_choice)

        def update_counts_for_bias_update():
            self.increase_total_years_and_tag_counts(other_player.get_tag(), own_payoff)
            other_player.increase_total_years_and_tag_counts(self.get_tag(), other_payoff)

            self.update_cooperator_count(other_choice, other_player.get_tag())
            other_player.update_cooperator_count(own_choice, self.get_tag())

        # --------------------- ACTUAL FUNCTION ----------------------

        assert other_player.id in self.network[self.id]

        # Each node chooses its tactic
        own_choice, other_choice = choose_tactics()

        # Compute the payoff from playing with the other node
        own_payoff, other_payoff = compute_payoffs()

        update_counts_for_bias_update()

    def choose_tactic(self, other_player):
        """
        Chooses tactic according to how much we like our own tag.
        """
        own_cooperate_prob = 1 - self.belief if self.tag == other_player.get_tag() else self.belief

        return np.random.choice(a=['C', 'D'], p=[own_cooperate_prob, 1 - own_cooperate_prob])

    def compute_payoff(self, own_choice, other_choice):
        inc = 0

        if own_choice == other_choice:
            if own_choice == 'C':
                inc = 1
            else:
                inc = 2
        elif own_choice == 'C':
            inc = 3
        
        self.round_total_payoff += inc
        
        return inc

    def update_belief(self):
        def delta():
            return (1 / self.other_tag_count) * self.other_tag_inv_payoff - (1 / self.own_tag_count) * self.own_tag_inv_payoff

        self.belief = sigmoid(self.belief * self.FORGETTING_FACTOR + delta())

        if self.belief > 0.5:
            self.tag = 1 - self.tag
            self.belief = 1 - self.belief

    # ---------------------- HELPER FUNCTIONS -----------------------

    def increase_total_years_and_tag_counts(self, other_node_tag, payoff):
        if other_node_tag == self.get_tag():
            self.own_tag_inv_payoff += 1 / (payoff + 1)
            self.own_tag_count += 1
        else:
            self.other_tag_inv_payoff += 1 / (payoff + 1)
            self.other_tag_count += 1
    
    def update_cooperator_count(self, other_choice, other_tag):
        if other_choice == 'C':
            if other_tag == self.get_tag():
                self.own_tag_cooperators += 1
            else:
                self.other_tag_cooperators += 1

    def reset_counters(self):
        self.own_tag_cooperators = self.other_tag_cooperators = 0
        self.own_tag_inv_payoff = self.other_tag_inv_payoff = 0
        self.own_tag_count = self.other_tag_count = 0

    
    def get_players(self, belief=None, just_neighbors=False):
        if just_neighbors:
            players = Player.network.neighbors(self.id)
        else:
            players = Player.network.nodes()

        if belief is None:
            return [Player.network.node[_]['player'] for _ in players]
        else:
            return [Player.network.node[_]['player'] for _ in players
                    if Player.network.node[_]['player'].belief['id'] == belief]

    def get_player(self, player_id):
        return Player.network.node[player_id]['player']

    def get_tag(self):
        return self.tag

    def get_other_tag_count(self):
        return self.other_tag_count
    
    def get_other_tag_cooperators(self):
        return self.other_tag_cooperators