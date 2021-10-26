from networkx.classes.graph import Graph
import simpy
import networkx as nx
from .player import Player

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
        opinions = []       # A list of dictionaries for each timestep, with opinions for each id
        global_biases = []  # A list of lists for each timestep, with prejudice for each pair
                            # That is, the table P for AA, AB, BA and BB

        # Running the simulation for num_timesteps
        for i in range(0, num_timesteps):
            # Play the game
            for u, v in [edge for edge in self.G.edges]:
                self.G[u]['player'].play_with_neighbour(self.G[v]['player'])

            # Update the individual biases after each round
            for u in self.G.nodes:
                self.G[u]['player'].update_bias()

            # TODO: Update global biases with the average of each tag's beliefs.
            # TODO: Resets counters.

            #Store statistics: current global bias and all players opinion
            global_biases += Player.global_bias

            currentOpinions = []
            for node in self.G.nodes:
                currentOpinions += [node['player'].get_tag()]
            
            opinions.append(currentOpinions)
    
        return opinions, global_biases