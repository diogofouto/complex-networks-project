import simpy
import networkx as nx

class Arena(simpy.Environment):
    def __init__(self, topology):
        super().__init__(initial_time=0)
        assert isinstance(topology, nx.Graph)
        self.G = topology