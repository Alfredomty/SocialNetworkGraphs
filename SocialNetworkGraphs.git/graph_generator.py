import math
import numpy as np
import networkx as nx
class GraphGenerator:

    @staticmethod
    def generate_erdos_graph(n, c):
        """
        Generates a random Erdos Reyni graph based on n and c values
        Params:
            n: integer value
            c: float value
        Returns
            G: a graph object """
    
        #Computes the probability p based on c and n
        p = c * (math.log(n) / n) if n > 1 else 0

        #Generating a erdos reyni graph with integers as nodes
        G = nx.erdos_renyi_graph(n, p)

        return G
    
    @staticmethod
    def generate_karate():
        """Generates a Karate Club graph
        Params:
            none
        Returns
            G: a graph object"""
        G = nx.karate_club_graph()
        
        return G

    @staticmethod
    def generate_bipartite(n,m,p):
        """
        Crates a random bipartite graph based on n, m and probability values
        Params:
            n: number of nodes in A
            m: number of nodes in B 
            p: probability of edge u,v between A u and B v 
        Returns:
            G: bipartite graph
        """
        G = nx.bipartite.random_graph(n,m,p)

        return G

    #Market clearing
    @staticmethod
    def generate_market(file_name):
        """Generates a standard market clearing graph
        Params:
            file_name: name of the file that incluides the info for the market clearing graph
        Returns:
            prices: price of the house 
            valuation: homeowner valuation of the house
            G: market clearing graph with no computations"""
        #Open file
        with open(file_name, 'r') as file:
            lines = file.readlines()
            n = int(lines[0].split()[0])
            prices = list(map(int, lines[0].split()[1].split(',')))
            valuations = np.array([list(map(int, line.split(','))) for line in lines[1:]])

        #Initialize a graph that just has the House and buyer prices and valuations in case someone wants to see it
        G = nx.Graph()
        for i in range(n):
            G.add_node(f"House {i+1}", bipartite=0)  # House nodes
        
        for j in range(valuations.shape[0]):
            G.add_node(f"Buyer {j+1}", bipartite=1)  # Buyer nodes
        
        # Add edges for buyers' highest valuations only
        for j in range(valuations.shape[0]):
            max_valuation = max(valuations[j])
            for i in range(n):
                if valuations[j, i] == max_valuation:
                    G.add_edge(f"House {i+1}", f"Buyer {j+1}")
                    break  # Move to the next buyer after connecting to the highest valued house
                
        return n, prices, valuations, G