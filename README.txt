CRC Project - Community Building and Segregation through Prisoner's Dilemma - Source Code

By Alexandre Pires - 92414, Diogo Fouto - 93705 and João Fonseca - 92497

-------------- CODE STRUCTURE ------------

The code is organized as follows:

- main.p:   This is where each main component is called: making the graph, running the simulation, and printing results. 
            Here, the graph is generated, as our code agnostic to the type of graph given.
            A new simulation is made using the given topology, using a given numbers of timesteps and attempts.
            The simulation is ran, returning lists of individual opinions and group biases, by attempt and by timestep.
            The results are then using to print plots, using the methods made in statistics.py.

- simulation.py:    This component is used as a facade for the arena, making it easier to run any given number of 
                    attempts of the simulation. It is also responsible for making instances of the player class associated
                    with each node in the graph, and running the simulation afterwards, using the Arena component.
                    The individual and community biases obtained for each timestep, of each attempt, are then sent back to main. 

- arena.py: The arena is responsible for handling anything related to the experience that is not focused on individual nodes.
            That means it not only updates the prejudice table (named global bias, in the code), but is it also responsible for
            making each player play the game with each neighbor (using the edges to avoid repetitions), and afterwards asking
            each player to update their individual beliefs. 
            arena.py also contains the starting community biases, in the matrix 'INIT_GLOBAL_BIAS', with the format [[AA,AB],[BB,BA]]
            It is also responsible for storing past individual beliefs and prejudice tables, and giving them to simulation.py 
            after running.

- player.py:    player.py is responsible for anything in the simulation that is based on the individual node level.
                This includes picking the tactic for each game, updating the individual payoff, updating cooperation 
                and defection counters, and updating the individual belief.
                As games are made for each edge, one player is also responsible for calculating the other's tactic,
                using the other player's stored experiences.

- utils.py: utils simply contains the code for the update formula for the biases.

- statistics.py:    This is where all the code related to plotting various results is kept.
                    Plots can be made for individual opinions or community biases, with some for a specific timestep,
                    and others for a collection of various attempts.

The various results obtained for the report are stored in the results folder, with the following naming schema:
AA-AB-BB-BA X, where X is related to the specific plot at hand: X=1 for community bias, X=2 for average individual belief, 
and X=3 for average number of players in each tag.


--------- RUNNING INSTRUCTIONS ------------

The following packages are needed to correctly run the project, the following python3 packages are needed:
networkx, numpy, matplotlib, simpy.

In order to run the code, main.py can simply be executed without no additional parameters.

In order to customize the simulation, the following variables can be ajusted:

main.py:
    num_of_nodes - The number of nodes the generated graph should have. Default: 1000
    G - The type of graph to be made, where any networkx undirected graph can be used. Default: barabasi_albert with avg_deg = 6
    num_attempts - The number of repetitions for the simulation, to achieve statistical relevance. Default: 30
    num_timesteps - The number of timesteps to be simulated for each attempt. Default: 200
arena.py:
    INIT_GLOBAL_BIAS - The initial matrix for community biases, in the format [[AA,AB],[BB,BA]].
player.py:
    OLD_BIAS_WEIGHT -   The weight given to the past timestep's bias, and the current timestep experience, when calculating
                        the evolution for the bias. Equivalent to the report's Wo. Default: 0.95
                    
