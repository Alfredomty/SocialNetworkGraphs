#Angel Grano-Cruz
#CECS 427
#Github version
import numpy as np
import dwave_networkx as dnx

from graph_manager import GraphManager
from graph_generator import GraphGenerator
from algos import Algos
from plot import Plot
from graph_attributes import Attributes
##ATTRIBUTES##


def print_main_menu():
    print("\nGraph Program - Main Menu")
    print("-------------------------")
    print("1. Read a graph from a file")
    print("2. Read a digraph from a file")
    print("3. Save the graph to a file")
    print("4. Create a graph")
    print("5. Graph algorithms")
    print("6. Plot the Graph")
    print("7. Assign and validate attributes")
    print("x. Exit")

def create_graph_menu(G,n,valuations, prices,assignment,payoffs,shortest_path):
    print("A. Random Erdos_Renyi Graph\nB. Karate-Club Graph\nC.Bipartite Graph\nD.Market-Clearing")
    graph_choice = input()
    G=G
    valuations=valuations
    prices=prices
    assignment=assignment
    payoffs = payoffs
    shortest_path = shortest_path

    #Erdos
    if graph_choice.upper() == 'A':
        n = int(input("Enter the number of nodes (n): "))
        c = float(input("Enter constant (c): "))
        G = GraphGenerator.generate_erdos_graph(n, c)
        # Initialize p 
        p = np.random.random()
        # Reset shortest path
        shortest_path = None  
        print("Random Erdos-Renyi graph created.")

    #Karate
    elif graph_choice.upper() == 'B':
        G = GraphGenerator.generate_karate()
        # Initialize p 
        p = np.random.random()
        #Reset shortest path
        shortest_path = None
        print("Karate Club graph created")
    #Bipartite
    elif graph_choice.upper() == 'C':
        n = int(input("Enter the number of nodes in A (n): "))
        m = int(input("Enter the number of nodes in B (m): "))
        p = float(input("Enter the probability of edge (p): "))
        G = GraphGenerator.generate_bipartite(n,m,p)
        shortest_path = None
        print("Bipartite graph created")
    #Market clearing
    elif graph_choice.upper() == 'D':
        file_name = input("Enter the file name: ")
        n, prices, valuations, G = GraphGenerator.generate_market(file_name)
        print("Market Clearing graph created")
    #Wrong input
    else:
        print("Invalid input")

def algorithms_menu(G,shortest_path):
    G= G
    shortest_path = shortest_path
    if G is not None:
        print("A. Shortest path\nB. Partition graph\nC. Travel Equilibrium and Social Optimality\nD. Perfect matching\nE. Preferred-seller graph")
        algo_choice = input()
        #Shortest path
        if algo_choice.upper() == 'A':
            source = int(input("Enter the source node: "))
            target = int(input("Enter the target node: "))
            shortest_path = Algos.calculate_shortest(G, source, target)

        #Parition graph
        elif algo_choice.upper() == 'B':
            num_components = int(input("How many components?: "))
            Algos.partition(G, num_components)
            print("Graph has been partitioned")
        
        #Social Optima and Nash equilibrium
        elif algo_choice.upper() == 'C':
            n = int(input("How many drivers?(n):"))
            source = int(input("Enter the source node: "))
            destination = int(input("Enter the destination node: "))
            Algos.nash_social(n,source,destination,G)
        #Perfect matching
        elif algo_choice.upper() == 'D':
            assignment, payoffs, prices= Algos.perfect_matching(n,prices,valuations)
            print("Perfect matching calculated for graph")
        #Preferred-seller
        elif algo_choice.upper() == 'E':
            if assignment==None:
                print("Perfect matching not calculated, please calculate perfect matching first")
            else:
                print(prices)
                G = Algos.preferred_seller_graph(n,assignment,payoffs,prices)
                print(prices)
                print("Preferred-seller graph calculated, you can now plot the graph")
        else:
            print("Invalid input")
    else:
        print("No graph is currently loaded.")

def plot_graph_menu(G):
    graph_choice = 0
    if G is not None:
        while(graph_choice !=4):
            print("A. Enable/Disable shortest path\nB. Enable/Disable Cluster Coefficients\nC. Enable/Disable Neighbor Overlaps\nD. Plot Bipartite\nE. Preferred-Seller Graph\nx.Done")
            graph_choice = input()
        
            if graph_choice.upper() == 'A':
                plot_shortest = submenu_plot(plot_shortest)
                
            elif graph_choice.upper() == 'B':
                plot_cluster = submenu_plot(plot_cluster)
                
            elif graph_choice.upper() == 'C':
                plot_neighbor = submenu_plot(plot_neighbor)

            elif graph_choice.upper() == 'D':
                Plot.plot_bipartite(G)  
            elif graph_choice.upper() == 'E':
                Plot.plot_preferred_seller_graph(G,n)
            elif graph_choice.upper() == 'X':
                break
            
            else:
                print("Invalid input")
        Plot.plot_graph(G, shortest_path, plot_shortest, plot_cluster, plot_neighbor)

    else:
        print("No graph is currently loaded.")

def submenu_plot(type):
    """
    Submenu that enables disables different elements of the plot graph function
    Param:
        type: boolean flag
    Returns
        type: boolean flag"""
    
    if type == False:
        choice = input("Currently disabled, enable? (Y/N): ")
        if choice.upper() == 'Y':
            print("Enabled")
            type = True
            return type 

        elif choice.upper() == 'N':
            print("Staying disabled")
            return type

    elif type == True:
        choice = input("Currently enabled, disable? (Y/N): ")
        if choice.upper() == 'Y':
                print("Disabled")
                type = False
                return type 

        elif choice.upper() == 'N':
            print("Staying Enabled")
            return type   
    
if __name__ == "__main__":
    #These variables are left outside the loop so they carry over within menu items 
    G,n,valuations, prices,assignment,payoffs,shortest_path = None
    plot_shortest,plot_cluster,plot_neighbor = False
    p = 0
    
    while True:
        #Main Menu
        print_main_menu()
        #User input
        choice = input("Enter your choice: ")

        ##OPTIONS##

        #Read graph
        if choice == '1':
            file_name = input("Enter the file name: ")
            G = GraphManager.read_graph(file_name)
            #Reset shortest path
            shortest_path = None  
            print("Graph loaded from file.")

        #Read bigraph
        elif choice == '2':
            file_name = input("Enter the file name: ")
            G = GraphManager.read_digraph(file_name)
            #Reset shortest path
            shortest_path = None  
            print("Graph loaded from file.")

        #Save
        elif choice == '3':
            if G is not None:
                file_name = input("Enter the file name to save the graph: ")
                GraphManager.save_graph(G, file_name)
                print("Graph saved successfully.")
            else:
                print("No graph is currently loaded.")

        #Create graph
        elif choice == '4':
            create_graph_menu(G,n,valuations, prices,assignment,payoffs,shortest_path)
            
        #Algorithms
        elif choice == '5':
            algorithms_menu(G,shortest_path)

        #Plot graph
        elif choice == '6':
            plot_graph_menu(G)
            
        #Attributes        
        elif choice == '7':
            if G is not None:
                print("A.Homophily\nB.Balanced graph")
                attribute_choice = input()
                if attribute_choice.upper() == 'A':
                    Attributes.homophily(G,p)
                elif attribute_choice.upper() == 'B':

                    is_balanced, negative_edges = Attributes.balanced_graph(G,p)
                    if is_balanced:
                        print("Graph is balanced")
                    else:
                        print(f"Graph is not balanced as it has {negative_edges} extra negative edges")
            else:
                print("No graph is currently loaded. ")
        #Exit
        elif choice == 'x':
            break

        #Invalid choice 
        else:
            print("Invalid choice. Please try again.")
