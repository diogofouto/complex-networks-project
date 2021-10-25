import networkx as nx
import numpy as np
from .arena import Arena


class Player:

    # ---------------------- STATIC VARIABLES -----------------------

    network = None # where all players reside
    global_bias = [[0.5, 0.5], [0.5, 0.5]] # bias between tags


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

        # Initialize network
        Player.network = arena.G

        # For SimPy
        self.env = arena
        self.env.process(self.run())

    def run(self, other_player):
        while True:
            self.play_with_neighour(other_player)
            #! Gotta break this cycle with yields or events, somehow


    # --------------------- PRISONER'S DILEMMA ----------------------

    def play_with_neighbour(self, other_player):
        assert other_player.id in self.network[self.id]

        def choose_tactics():
            return self.choose_tactic(other_player), other_player.choose_tactic(self)

        def compute_payoffs():
            return self.compute_payoff(own_choice, other_choice), other_player.compute_payoff(other_choice, own_choice)

        def update_biases():
            self.update_bias(own_payoff, other_player.get_tag())
            other_player.update_bias(other_payoff, self.get_tag())
        
        def increase_total_years_and_tag_counts(own_tag_inv_years, own_tag_neighs,
                                                    other_tag_inv_years, other_tag_neighs,
                                                        own_previous_payoff):
            increase_in_years = self.round_total_payoff - own_previous_payoff

            if self.get_tag() != other_player.get_tag():
                other_tag_inv_years += 1 / increase_in_years
                other_tag_neighs += 1
            else:
                own_tag_inv_years += 1 / increase_in_years
                own_tag_neighs += 1

        # Each node chooses its tactic
        own_choice, other_choice = choose_tactics()

        # Compute the payoff from playing with the other node
        own_payoff, other_payoff = self.compute_payoff(own_choice, other_choice)
        
        update_biases()

    def choose_tactic(self, other_player):
        cooperate_prob = self.bias[self.get_tag()][other_player.get_tag()]
        return np.random.choice(a=['C', 'D'], p=[cooperate_prob, 1-cooperate_prob])

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

    def update_bias(self, payoff=None, other_player_tag=None):
        def compute_delta(self):
            return 
        pass

    # ---------------------- HELPER FUNCTIONS -----------------------
    
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
        return round(self.tag)