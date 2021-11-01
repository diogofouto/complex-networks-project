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
        # --------------------- AUXILIARY FUNCTIONS ----------------------

        def relative_defection(interactions_with_tag_x, def_tag_x):
            """
            Computes the relative defection of the tag y as experienced by the
            tag x.
            """
            #TODO CHECK THIS! 
            if (interactions_with_tag_x == 0):
                return 0

            ret = 2 * (def_tag_x / interactions_with_tag_x) - 1

            return ret

        def new_bias(prev_bias, rel_def):
            return sigmoid(prev_bias + rel_def)

        # --------------------- ACTUAL FUNCTION ----------------------

        inter_00 = inter_01 = 0
        inter_10 = inter_11 = 0

        defect_00 = defect_01 = 0
        defect_10 = defect_11 = 0

        for u in self.G.nodes:
            player: Player = self.G.nodes[u]['player']
            if player.get_tag() == 0:
                inter_00 += player.get_own_tag_count()
                inter_01 += player.get_other_tag_count()
                defect_00 += player.get_own_tag_count() - player.get_own_tag_cooperators()
                defect_01 += player.get_other_tag_count() - player.get_other_tag_cooperators()
            else:
                inter_11 += player.get_own_tag_count()
                inter_10 += player.get_other_tag_count()
                defect_11 += player.get_own_tag_count() - player.get_own_tag_cooperators()
                defect_10 += player.get_other_tag_count() - player.get_other_tag_cooperators()

        relative_def_0_0 = relative_defection(inter_00, defect_00)
        relative_def_1_1 = relative_defection(inter_11, defect_11)

        relative_def_0_1 = relative_defection(inter_01, defect_01)
        relative_def_1_0 = relative_defection(inter_10, defect_10)

        Player.global_bias[0][0] = new_bias(Player.global_bias[0][0], relative_def_0_0)
        Player.global_bias[0][1] = new_bias(Player.global_bias[0][1], relative_def_0_1)
        Player.global_bias[1][1] = new_bias(Player.global_bias[1][0], relative_def_1_1)
        Player.global_bias[1][0] = new_bias(Player.global_bias[1][1], relative_def_1_0)
