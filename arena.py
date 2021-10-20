import simpy
import networkx as nx
import Player

class Arena(simpy.Environment):
    def __init__(self, topology):
        super().__init__(initial_time=0)
        assert isinstance(topology, nx.Graph)
        self.G = topology

    """
    Run is overriden in order to get the list of the players after each timestep.

    Returns a list of the opinions and a list of global biases for each timestep
    """
    def run(self, num_timesteps):
        opinions = []# A list of dictionaries for each timestep, with opinions for each id
        global_biases = []    # A list of dictionaries for each timestep, with prejudice for each pair
                            # That is, the table P for AA, AB, BA and BB


        for i in range(0, num_timesteps):
            super.run(1)

            #Store statistics: current global bias and all players opinion
            global_biases += Player.global_bias

            currentOpinions = []
            for node in G.nodes:
                currentOpinions += [node['player'].tag]
            
            opinions.append(currentOpinions)
    
        return opinions, global_biases