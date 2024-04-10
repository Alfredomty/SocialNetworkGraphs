import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import dwave_networkx as dnx
from dwave.samplers import SimulatedAnnealingSampler
class Attributes:

    @staticmethod
    def homophily(G,p):
        """
        Calculates homophily in graph
        Param:
            G: a graph object
            p: probability of the graph
        Returns:
            none"""
        for node in G.nodes():
            G.nodes[node]['color'] = 'red' if np.random.rand() < p else 'blue'
        
        
        # Calculate and print the assortativity coefficient
        assortativity = nx.attribute_assortativity_coefficient(G, 'color')
        print(f"Assortativity coefficient: {assortativity}")

        #Plot the graph 
        colors = [G.nodes[node]['color'] for node in G.nodes()]
        nx.draw(G, node_color=colors, with_labels=True)
        plt.title("Homophily graph")
        plt.show()
        
    @staticmethod
    def balanced_graph(G,p):
        """
        Assigns + or - to edges in a graph and checks if the graph is balanced
        Param:
            G: a graph object
            p: probability of the graph
        Returns:
            is_balanced: boolean that is True if the graph is balanced
            num_frustrated_edges: Number of edges that are '-'
        """
        edge_labels = {}

        for edge in G.edges():
            # Set 'sign' attribute to '+' or '-'
            # Signs are in integers because the dnx function will not work without them
            # 1 for positive -1 for negative
            G.edges[edge]['sign'] = 1 if np.random.rand() < p else -1

            #Labeling edges with actual signs to display them correctly
            sign = G.edges[edge]['sign']
            edge_labels[edge] = '+' if sign == 1 else '-'

        # Initialize the sampler
        sampler = SimulatedAnnealingSampler()

        # Check structural imbalance
        try:
            imbalances= dnx.structural_imbalance(G, sampler)
            is_balanced = len(imbalances) == 0
            num_frustrated_edges = len(imbalances)  # Number of negative edges
        except Exception as e:
            print(f"Error checking structural imbalance: {e}")
            return None, None
        #Initializing position
        pos = nx.spring_layout(G)

        #Drawing nodes and labeling edges with different colors depending on sign
        nx.draw_networkx(G, pos, edge_color=[G[u][v]['sign'] for u,v in G.edges()], node_color='blue', with_labels=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green')

        #Showing
        plt.title("Graph with Signed Edges")
        plt.show()
        return is_balanced, num_frustrated_edges