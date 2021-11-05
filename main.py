#%%
import networkx as nx
from simulation import Simulation
import statistics

def main(num_of_nodes=1000):
	G = nx.barabasi_albert_graph(num_of_nodes, 6)
	
	# Run simulation
	sim = Simulation(topology=G, num_attempts=30, num_timesteps=200)
	beliefs, biases = sim.run()

	# Plot statistics
	statistics.plotBiasesByTimestep(biases)
	statistics.plotAvgBeliefByTimestep(beliefs)
	statistics.plot_players_by_tag_by_timestep(beliefs)

if __name__ == '__main__':
	main()
# %%
