import networkx as nx


# SIMULATION CONSTANTS
# to be thought about


def main(num_of_nodes=100):
    # Build Graph
    G = nx.barabasi_albert_graph(num_of_nodes)
    
    # Run Simulation
    sim = Simulation(topology=G)
    opinions, biases = sim.run()

    # Draw Visualization
    nx.draw(G)

    # Process statistics

if __name__ == '__main__':
    main()
