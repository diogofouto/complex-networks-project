import networkx as nx
from .simulation import Simulation


def main(num_of_nodes=100):
	# build graph
	G = nx.barabasi_albert_graph(num_of_nodes, 5)
	
	# run simulation
	sim = Simulation(topology=G)
	sim.run()

if __name__ == '__main__':
	main()