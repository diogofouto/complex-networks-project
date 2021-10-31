import numpy as np
#import networkx as nx
#from arena import Arena
from utils import sigmoid


class Player:

    # ---------------------- STATIC VARIABLES -----------------------
    network = None              # where all players reside
    global_bias = [[0.3, 0.5],[0.3, 0.5]]    # bias towards thinking that a player is a defector, according to his tag
                                             # Format: [[AA,AB],[BB,BA]]
    FORGETTING_FACTOR = 0.05

    # ----------------------- MAIN FUNCTIONS ------------------------

    def __init__(self, arena=None, player_id=None):
        # Check arguments
        assert arena is not None, TypeError('No arena given.')
        assert player_id is not None, TypeError('No player_id given.')

        # Newborn player params
        self.id = player_id
        self.belief = np.random.default_rng().uniform() # Random number between 0 and 1
        self.bias = Player.global_bias
        self.round_total_payoff = 0

        # 0 or 1
        self.tag = round(self.belief)

        # Parameters used to compute the belief and for bias updates

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
        self.env = arena
        self.env.process(self.run())


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
        Chooses tactic according to how much the player believes the other will collaborate.
        If the player believes the other will collaborate, 
        it will only do so as well based on how much the other player's belief is similar to his.
        """
        opponent_prediction = ""

        if (self.tag == other_player.get_tag()):
            opponent_prediction = np.random.default_rng().choice(a=['C', 'D'], p=[1 - self.bias[self.tag][0], self.bias[self.tag][0]])
        else:
            opponent_prediction = np.random.default_rng().choice(a=['C', 'D'], p=[1 - self.bias[self.tag][1], self.bias[self.tag][1]])

        #If we predict a defect, we defect too, else we roll a chance for deffection 
        if (opponent_prediction == 'D'):
            return 'D'
        else:
            chance_to_defect = abs(self.belief - other_player.belief)
            return np.random.default_rng().choice(a=['C', 'D'], p=[1 - chance_to_defect, chance_to_defect])


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
            #TODO GET BETTER RULE TO STOP DIVIDING BY 0
            if (self.other_tag_count == 0):
                return - (1 / self.own_tag_count) * self.own_tag_inv_payoff
            elif (self.own_tag_count == 0):
                return (1 / self.other_tag_count) * self.other_tag_inv_payoff
            return (1 / self.other_tag_count) * self.other_tag_inv_payoff - (1 / self.own_tag_count) * self.own_tag_inv_payoff

        self.belief = sigmoid(self.belief * self.FORGETTING_FACTOR + delta())
        
        if (self.belief > 0.5 and self.tag == 0) or (self.belief < 0.5 and self.tag == 1):
            self.tag = 1 - self.tag

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

    def get_own_tag_count(self):
        return self.own_tag_count

    def get_own_tag_cooperators(self):
        return self.own_tag_cooperators

    # ---------------------- MAIN RUNNING FUNCTION -----------------------

    def run(self):
        #! Should this really be while True?
        while True:
            self.play_with_neighbour()
            #! Is the below line correct?
            yield self.env.timeout(1) # each interaction takes 1 timestep