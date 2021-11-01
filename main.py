#%%
import networkx as nx
from simulation import Simulation
import statistics

def main(num_of_nodes=100):
	# build graph
	G = nx.watts_strogatz_graph(num_of_nodes, 5, 0.2)
	#G = nx.barabasi_albert_graph(num_of_nodes, 5)
	
	# run simulation
	sim = Simulation(topology=G, num_attempts=1)
	opinions, prejudices = sim.run()
	
	statistics.plotPrejudiceByTimestep(prejudices)
	#statistics.drawCumRoundedOpinions(opinions)

if __name__ == '__main__':
	main()
# %%
