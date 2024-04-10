
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

class Algos:
    
    @staticmethod
    #Shortest path 
    def calculate_shortest(G, source, target):
        """
        Computes the shortest path between two edges
        Params:
            G: graph object
            source: str
            target: str
        Returns
            path: dict """
        
        #Nx gives us a shortest path function
        try:
            path = nx.shortest_path(G, source=source, target=target)
            print("Shortest path:", ' -> '.join(str(path)))
            return path
        
        #Just in case the two nodes are not connected

        except nx.NetworkXNoPath:
            print("No path exists between", source, "and", target)
            return None

    @staticmethod
    #Partition
    def partition(G, num_components):
        """
        Removes edges with the highest betweenness until the number of connected components is num_components
        Params:
            G: a graph object
            num_components: desired number of connected components"""
        while nx.number_connected_components(G) < num_components:
            # Calculate edge betweenness centrality
            edge_betweenness = nx.edge_betweenness_centrality(G)
            # Find the edge with highest
            max_edge = sorted(edge_betweenness.items(), key=lambda x: x[1], reverse=True)[0][0]
            # Remove the edge
            G.remove_edge(*max_edge)

   
    #Nash equilibrium and Social optima
    def travel_time(self,G, x, edge):
        """
        Calulates travel time for an edge based on a given flow in the form ax+b
        Param:
            G: graph Object
            x: velocity of a node
            edge: edge being looked at
        
        Returns:
            travel time in form a*x+b
        """
        weight = G.edges[edge].get('weight')

        if not isinstance(weight, (list, tuple)) or len(weight) != 2:
            raise ValueError(f'Edge weight format is incorrect for edge {edge}: {weight}')
        
        a,b= weight
        return a*x +b
    
    
    def adjust_nash_flows(self, G, path_flows,n):
        """
        Adjusts path flows towards a Nash equlibrium
        Param: 
            G: graph Object
            path_flows: tuple of nodes
        Returns:
            path_flows: new tuple of nodes for the flow of traffic
        """
        max_path, min_path = None,None
        #Setting up really low numbers for comparison
        max_time, min_time = float('-inf'), float('inf')

        for path,flow in path_flows.items():
            #Calculate total time for edges
            edges = zip(path, path[1:])
            time = sum(self.travel_time(G,flow,edge) for edge in edges)
            #Find the max and min times and paths associated 
            if time > max_time:
                max_time, max_path = time,path
            if time< min_time:
                min_time, min_path = time, path
        
        #Shifts 10% of drivers from max to min path
        if max_path and min_path and max_path != min_path:
            adjustment = min(path_flows[max_path] * 0.1, n)
            path_flows[max_path] -= adjustment
            path_flows[min_path] += adjustment

        return path_flows

    def nash_social(self,n,source,destination,G):
        """
        """
        #Create a list of simple paths from G
        paths = list(nx.all_simple_paths(G, source, destination))
        #Partition the list for the nash equilibrium and social optima calculations
        path_flows_nash = {tuple(path): n / len(paths) for path in paths}
        path_flows_social = path_flows_nash.copy()

        #Iterate through the paths to try to get an equilibrium
        for _ in range(100):
            prev_flows = path_flows_nash.copy()
            path_flows_nash = self.adjust_nash_flows(G,path_flows_nash,n)
            #If there isnt much change end the iterations
            if all(prev_flows[path] == flow for path, flow in path_flows_nash.items()):
                break

        #Calculate the total time for plotting
        nash_total_time = sum(sum(self.travel_time(G, path_flows_nash[path], (u, v)) for u, v in zip(path, path[1:])) * path_flows_nash[path] for path in path_flows_nash)

        #Social optima calculation
        #Calculate the sum of the paths
        path_times ={tuple(path): sum(self.travel_time(G, 1, (u, v)) for u, v in zip(path, path[1:])) for path in paths}
        #Get the sum of the inverse of time from paths
        total_inverse_time = sum(1 / time for time in path_times.values())
        path_flows_social = {tuple(path): (1 / path_times[tuple(path)]) / total_inverse_time * n for path in paths}

        #Calculate the total time for plotting
        social_total_time = sum(sum(self.travel_time(G, path_flows_social[path], (u, v)) for u, v in zip(path, path[1:])) * path_flows_social[path] for path in path_flows_social)

        #Plot
        labels = ['Nash Equilibrium', 'Social Optimum']
        values = [nash_total_time, social_total_time]
        
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=['blue', 'red'])
        plt.ylabel('Total Travel Time')
        plt.title(f'Total Travel Time Comparison for {n} Drivers')
        plt.show()

    @staticmethod
    #Perfect matching
    def perfect_matching(n, prices, valuations):
        """
        Creates a perfect match of buyers and sellers based on payoffs
        Params:
            n: number of buyer/sellers
            prices: list of seller prices, initialized to 0
            valuations: 2-D list of buyer valuations for each house
        Returns:
            assignment: Combination of correct buyer to seller
            payoffs: list of final buyer payoffs
            prices: list of final prices
        """
        #Initialize assignments and payoffs
        assignment = [-1] * n
        payoffs = [0] * n
        #Flag
        resolved = False

        while not resolved:
            #Assume this iteration will resolve all conflicts unless found otherwise
            resolved = True
            new_assignment = [-1] * n
            new_payoffs = [0] * n

            #Calculate payoffs and tentative assignments for each buyer
            for i in range(n):
                best_payoff = -float('inf')
                for j in range(n):
                    payoff = valuations[i][j] - prices[j]
                    if payoff > best_payoff:
                        best_payoff = payoff
                        new_assignment[i] = j
                        new_payoffs[i] = payoff

            #Detect and resolve conflicts by adjusting prices
            for i in range(n):
                for j in range(i + 1, n):
                    if new_assignment[i] == new_assignment[j] and new_assignment[i] != -1:
                        # Conflict detected, increment price to resolve
                        prices[new_assignment[i]] += 1
                        resolved = False  #Need another iteration to re-evaluate assignments

            # Update the assignments and payoffs after each iteration
            assignment = new_assignment.copy()
            payoffs = new_payoffs.copy()
        

        return assignment, payoffs, prices

    @staticmethod
    #Prefered seller
    def preferred_seller_graph(n, assignment, payoffs, prices):
        """
        Generates the prefered seller graph given the perfect match
        Params:
            n: number of buyer/sellers
            assignment: Combination of correct buyer to seller
            payoffs:  list of final buyer payoffs
            prices: list of final prices
        Returns:
            G: prefered seller graph
        """
        G = nx.DiGraph()

        #Buyers
        G.add_nodes_from(range(n), bipartite=0)
        # Add seller nodes with price attributes
        for i, price in enumerate(prices):
            G.add_node(n + i, bipartite=1, price=price)

        # Add edges based on assignments and payoffs
        for i, seller in enumerate(assignment):
            payoff_text = f"Payoff: {payoffs[i]}"
            G.add_edge(i, n+seller, weight=payoff_text)
        
        return G

