import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

class Plot:
    
    #Normal graph
    @staticmethod
    def plot_graph(G, shortest_path, plot_shortest, plot_cluster, plot_neighbor):
        """
        Creates the graph into a nx window
        Params:
            G: graph object
            shortest_path: an nx object that dictates the shortest path to a node
            plot_shortest: Boolean flag to plot shortest path
            plot_cluster : Boolean flag to plot node sizes and colors based on cluster coefficents
            plot_neighbor: Boolean flag to highlight neighborhood overlaps
        Returns
            None """
        #Source: https://stackoverflow.com/questions/29797990/networkx-spring-layout-with-different-edge-values
        initialpos = {1:(0,0), 2:(0,3), 3:(0,-1), 4:(5,5)}
        #Seed allows us to keep the graph the same from each iteration
        pos = nx.spring_layout(G, pos=initialpos, seed= 420, weight=None)
        nx.draw(G, pos, with_labels=True, font_weight='bold')

        #Cluster coefficients 
        max_pixel = 1000
        min_pixel = 100
        if plot_cluster:
            #Cluster function from nx
            cluster_coefficients = nx.clustering(G)
            cluster_min, cluster_max = min(cluster_coefficients.values()), max(cluster_coefficients.values())

            for node, cc in cluster_coefficients.items():
                pv = (cc - cluster_min) / (cluster_max - cluster_min) if cluster_max > cluster_min else 0
                nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=min_pixel + pv * (max_pixel - min_pixel), node_color=[(pv, (1 - pv), 0)], alpha=0.8)

        #Shortest path
        if shortest_path and plot_shortest:
            path_edges = list(zip(shortest_path, shortest_path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=1, style='dotted')
        
        #Neighbor overlaps
        if plot_neighbor:
            for u,v in G.edges():
                common_neighbors = len(list(nx.common_neighbors(G,u,v)))
                if common_neighbors > 0:
                    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='y', width=1 + common_neighbors *0.8, alpha = 0.5)
        plt.show()

    #Digraph
    @staticmethod
    def plot_digraph(G):
        """
        Plots the graph
        Param:
            G: graph
        Returns: 
            None """
        pos = nx.spring_layout(G, weight=None)
        #Nodes
        nx.draw_networkx_nodes(G,pos, node_size = 600, node_color = 'lightblue')
        #Edges
        nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowsize=20)
        #Labels
        nx.draw_networkx_labels(G, pos)
        #Create the labels to show the weights and draw
        edge_labels = {(u, v): '{}x + {}'.format(data['weight'][0], data['weight'][1]) for u, v, data in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        plt.show()

    #Prefered seller graph
    def plot_preferred_seller_graph(G,n):
        """
        Plots the prefered seller graph 
        Params:
            n: number of buyer sellers
            G: graph object
        Returns: 
            None
        """
        plt.figure(figsize=(10, 8))

        #Manual positioning of nodes to align them side by side
        pos = {}
        buyer_y_positions = [1 - (i / (n - 1)) for i in range(n)] if n > 1 else [0.5]
        seller_y_positions = [1 - (i / (n - 1)) for i in range(n)] if n > 1 else [0.5]
        
        for i, node in enumerate(G.nodes):
            if G.nodes[node]['bipartite'] == 0:  # Buyer
                pos[node] = (0, buyer_y_positions.pop(0))
            else:  # Seller
                pos[node] = (1, seller_y_positions.pop(0))

        #Classifying and drawing nodes
        buyer_nodes = [node for node in G.nodes if G.nodes[node]['bipartite'] == 0]
        seller_nodes = [node for node in G.nodes if G.nodes[node]['bipartite'] == 1]

        node_labels = {}
        for node in G.nodes:
            if node in buyer_nodes:
                node_labels[node] = f"B{node + 1}"
            else:
                node_labels[node] = f"S{node - len(buyer_nodes) + 1} \nPrice: {G.nodes[node]['price']}"

        nx.draw_networkx_nodes(G, pos, nodelist=buyer_nodes, node_color='blue', label='Buyers', node_size=2500)
        nx.draw_networkx_nodes(G, pos, nodelist=seller_nodes, node_color='green', label='Sellers', node_size=2500)

        # Drawing edges and labels
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos, labels=node_labels)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,label_pos=0.7)

        plt.title("Preferred Seller Graph")
        plt.axis('off')
        plt.show()

    #Bipartite plot
    @staticmethod
    def plot_bipartite(G):
        """
        Plots a bipartite graph.
        Params:
            G: bipartite graph
        Returns:   
            None
        """
        # Check if the graph is bipartite
        if not nx.is_bipartite(G):
            raise ValueError("The graph is not bipartite.")
        
        # Get the two node sets
        nodes_A, nodes_B = nx.bipartite.sets(G)
        
        # Define positions using the bipartite layout
        pos = nx.bipartite_layout(G, nodes_A)

        # Draw the nodes and edges
        nx.draw(G, pos, with_labels=True, node_color=['blue' if node in nodes_A else 'green' for node in G.nodes()], edge_color='gray')
        
        plt.title("Bipartite Graph")
        plt.show()