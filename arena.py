from copy import deepcopy
import simpy
import networkx as nx
from player import Player
from utils import sigmoid
from networkx.classes.graph import Graph

class Arena(simpy.Environment):
    def __init__(self, topology: Graph):
        assert isinstance(topology, nx.Graph)
        super().__init__(initial_time=0)
        self.G = topology

    def run(self, num_timesteps):
        """
        Run is overriden in order to get the list of the players after each timestep.
        Returns a list of the opinions and a list of global biases for each timestep
        """
        
        # --------------------- AUXILIARY FUNCTION ----------------------

        def update_biases():
            # Update of the global and individual biases
            self.update_global_biases()

            # Update the individual biases after each round and resets their counters
            for u in self.G.nodes:
                player = self.G.nodes[u]['player']

                player.update_belief()
                player.reset_counters()
        
        # --------------------- ACTUAL FUNCTION ----------------------

        opinions = [] # opinions of each id for each timestep
        global_biases = [deepcopy(Player.global_bias.copy())] # global biases for each timestep (i.e. the table P for AA, AB, BA and BB)

        for i in range(num_timesteps):
            #super().run(until=i + 1)

            # Running the simulation for num_timesteps

            for u, v in [edge for edge in self.G.edges]:
                p_1 = self.G.nodes[u]['player']
                p_2 = self.G.nodes[v]['player']

                p_1.play_with_neighbour(p_2)

            update_biases()

            # Store statistics: current global bias and all players opinion
            global_biases.append(deepcopy(Player.global_bias))

            current_opinions = []
            for n in self.G.nodes():
                current_opinions.append(self.G.nodes[n]['player'].get_tag())
        
        return current_opinions, global_biases

    def update_global_biases(self):
        #! This function is turning into a *big* mess...

        # --------------------- AUXILIARY FUNCTIONS ----------------------

        def relative_defection(players_of_tag_x, fraction_coop_tag_y, fraction_def_tag_y):
            """
            Computes the relative defection of the tag y as experienced by the
            tag x.
            """
            #TODO CHECK THIS! 
            if (players_of_tag_x == 0):
                return 0

            return (1 / players_of_tag_x) * (fraction_def_tag_y - fraction_coop_tag_y)

        def fraction_of_other_tag_coops(p: Player):
            coops = p.get_other_tag_cooperators()
            neighs = p.get_other_tag_count()

            return coops / neighs if neighs != 0 else 0

        def fraction_of_other_tag_defactors(p: Player):
            defactors = p.get_other_tag_count() - p.get_other_tag_cooperators()
            neighs = p.get_other_tag_count()

            return defactors / neighs if neighs != 0 else 0

        def fraction_of_own_tag_coops(p: Player):
            coops = p.get_own_tag_cooperators()
            neighs = p.get_own_tag_count()

            return coops / neighs if neighs != 0 else 0

        def fraction_of_own_tag_defactors(p: Player):
            defactors = p.get_own_tag_count() - p.get_own_tag_cooperators()
            neighs = p.get_other_tag_count()

            return defactors / neighs if neighs != 0 else 0

        def new_bias(prev_bias, rel_def):
            return sigmoid(prev_bias + rel_def)

        # --------------------- ACTUAL FUNCTION ----------------------

        total_0_players = 0
        total_1_players = 0
        tag_0_sum_fraction_of_0_coops = tag_0_sum_fraction_of_1_coops = 0
        tag_1_sum_fraction_of_0_coops = tag_1_sum_fraction_of_1_coops = 0
        tag_0_sum_fraction_of_0_def = tag_0_sum_fraction_of_1_def = 0
        tag_1_sum_fraction_of_0_def = tag_1_sum_fraction_of_1_def = 0

        for u in self.G.nodes:
            player = self.G.nodes[u]['player']
            if player.get_tag() == 0:
                total_0_players += 1
                tag_0_sum_fraction_of_0_coops += fraction_of_own_tag_coops(player)
                tag_0_sum_fraction_of_0_def += fraction_of_own_tag_defactors(player)
                tag_0_sum_fraction_of_1_coops += fraction_of_other_tag_coops(player)
                tag_0_sum_fraction_of_1_def += fraction_of_other_tag_defactors(player)
            else:
                total_1_players += 1
                tag_1_sum_fraction_of_1_coops += fraction_of_own_tag_coops(player)
                tag_1_sum_fraction_of_1_def += fraction_of_own_tag_defactors(player)
                tag_1_sum_fraction_of_0_coops += fraction_of_other_tag_coops(player)
                tag_1_sum_fraction_of_0_def += fraction_of_other_tag_defactors(player)

        relative_def_0_0 = relative_defection(total_0_players, tag_0_sum_fraction_of_0_coops, tag_0_sum_fraction_of_0_def)
        relative_def_1_1 = relative_defection(total_1_players, tag_1_sum_fraction_of_1_coops, tag_1_sum_fraction_of_1_def)

        relative_def_0_1 = relative_defection(total_0_players, tag_0_sum_fraction_of_1_coops, tag_0_sum_fraction_of_1_def)
        relative_def_1_0 = relative_defection(total_1_players, tag_1_sum_fraction_of_0_coops, tag_1_sum_fraction_of_0_def)

        Player.global_bias[0][0] = new_bias(Player.global_bias[0][0], relative_def_0_0)
        Player.global_bias[0][1] = new_bias(Player.global_bias[0][1], relative_def_0_1)
        Player.global_bias[1][1] = new_bias(Player.global_bias[1][0], relative_def_1_1)
        Player.global_bias[1][0] = new_bias(Player.global_bias[1][1], relative_def_1_0)
