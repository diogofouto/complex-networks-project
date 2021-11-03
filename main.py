#%%
import networkx as nx
from simulation import Simulation
import statistics

def main(num_of_nodes=100):
	G = nx.barabasi_albert_graph(num_of_nodes, 2)
	
	# Run simulation
	sim = Simulation(topology=G, num_attempts=3)
	beliefs, biases = sim.run()

	# Plot statistics
	statistics.plotPrejudiceByTimestep(biases)
	# statistics.plotOpinions(beliefs)

if __name__ == '__main__':
	main()
# %%
