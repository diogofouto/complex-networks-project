import networkx as nx
from simulation import Simulation
import statistics

def main(num_of_nodes=100):
	# build graph
	G = nx.barabasi_albert_graph(num_of_nodes, 5)
	
	# run simulation
	sim = Simulation(topology=G)
	opinions, prejudices = sim.run()

	statistics.plotPrejudiceByTimestep(prejudices)

if __name__ == '__main__':
	main()