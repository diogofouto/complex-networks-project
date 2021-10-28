from networkx.classes.graph import Graph
import simpy
import networkx as nx
from .player import Player
from .utils import sigmoid

class Arena(simpy.Environment):
    def __init__(self, topology: Graph):
        super().__init__(initial_time=0)
        assert isinstance(topology, nx.Graph)
        self.G = topology

    """
    Run is overriden in order to get the list of the players after each timestep.

    Returns a list of the opinions and a list of global biases for each timestep
    """
    def run(self, num_timesteps):
        
        # --------------------- AUXILIARY FUNCTION ----------------------

        def update_biases():
            # Update of the global and individual biases
            self.update_global_biases()

            # Update the individual biases after each round and resets their counters
            for u in self.G.nodes:
                player = self.G[u]['player']

                player.update_bias()
                player.reset_counters()
        
        # --------------------- ACTUAL FUNCTION ----------------------

        opinions = []       # A list of dictionaries for each timestep, with opinions for each id
        global_biases = []  # A list of lists for each timestep, with prejudice for each pair
                            # That is, the table P for AA, AB, BA and BB

        # Running the simulation for num_timesteps
        for i in range(0, num_timesteps):
            # Play the game
            for u, v in [edge for edge in self.G.edges]:
                p_1 = self.G[u]['player']
                p_2 = self.G[v]['player']

                p_1.play_with_neighbour(p_2)

            update_biases()

            # Store statistics: current global bias and all players opinion
            global_biases += Player.global_bias

            currentOpinions = []
            for node in self.G.nodes:
                currentOpinions += [node['player'].get_tag()]
            
            opinions.append(currentOpinions)
    
        return opinions, global_biases

    def update_global_biases(self):

        # --------------------- AUXILIARY FUNCTIONS ----------------------

        def relative_cooperation(players_of_tag_x, fraction_coop_tag_y):
            """
            Computes the relative cooperation of the tag y as experienced by the
            tag x.

            Since the fraction of defactors will be 1 minus the fraction of 
            cooperators, we have that the relative cooperation is given by:
                rc  = (1 / total(tag_x)) * (fc - fd) =
                    = (1 / total(tag_x)) * (fc - (1 - fc))
                    = (1 / total(tag_x)) * (2fc - 1)
            """
            return (1 / players_of_tag_x) (2 * fraction_coop_tag_y - 1)
        def fraction_of_other_tag_coops(p: Player):
            coops = p.get_other_tag_cooperators()
            neighs = p.get_other_tag_count()
            return coops / neighs
        def new_bias(prev_bias, rel_coop):
            return sigmoid(prev_bias + rel_coop)

        # --------------------- ACTUAL FUNCTION ----------------------

        total_0_players = 0
        total_1_players = 0
        tag_0_sum_fraction_of_1_coops = 0
        tag_1_sum_fraction_of_0_coops = 0

        for u in self.G.nodes:
            player = self.G[u]['player']
            if player.get_tag() == 0:
                total_0_players += 1
                tag_0_sum_fraction_of_1_coops += fraction_of_other_tag_coops(player)
            else:
                total_1_players += 1
                tag_1_sum_fraction_of_0_coops += fraction_of_other_tag_coops(player)

        relative_coop_0_1 = relative_cooperation(total_0_players, tag_0_sum_fraction_of_1_coops)
        relative_coop_1_0 = relative_cooperation(total_1_players, tag_1_sum_fraction_of_0_coops)
        
        Player.global_bias = new_bias(Player.global_bias[0], relative_coop_0_1)
        Player.global_bias = new_bias(Player.global_bias[1], relative_coop_1_0)
