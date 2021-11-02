#%%
import networkx as nx
from simulation import Simulation
import statistics

def main(num_of_nodes=1000):
	# build graph
	#G = nx.watts_strogatz_graph(num_of_nodes, 5, 0.6)
	G = nx.barabasi_albert_graph(num_of_nodes, 2)
	
	# run simulation
	sim = Simulation(topology=G, num_attempts=1)
	opinions, prejudices = sim.run()
	
	statistics.plotPrejudiceByTimestep(prejudices)
	statistics.plotOpinions(opinions)

if __name__ == '__main__':
	main()
# %%
