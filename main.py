import networkx as nx

# SIMULATION CONSTANTS
#    to be filled

def main(num_of_nodes=100):
    # Build Network
    G = nx.barabasi_albert_graph(num_of_nodes)
    players_states = [{'id': 0, } for _ in range(num_of_nodes)]
    
    # Run Simulation
    sim = Simulation(topology=G, agents=players_states, agent_type=Player)
    sim.run_sim()

    # Draw Visualization
    nx.draw(G)

if __name__ == '__main__':
    main()
