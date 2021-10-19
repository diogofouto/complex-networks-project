import networkx as nx


# SIMULATION CONSTANTS
# to be thought about


def main(num_of_nodes=100):
    # Build Network
    G = nx.barabasi_albert_graph(num_of_nodes)
    players_info = [{'id': 0, } for _ in range(num_of_nodes)]
    
    # Run Simulation
    sim = Simulation(topology=G, players_info=players_info)
    sim.run()

    # Draw Visualization
    nx.draw(G)

if __name__ == '__main__':
    main()
