import networkx as nx
class GraphManager:
    def __init__(self):
        """
        Initializes the GraphManager instance.
        """
        pass  # No initialization required for now, but method is defined for future extensibility.

    @staticmethod
    def read_graph(file_name):
        """
        Reads an undirected graph from a given file.

        Params:
            file_name: string
        Returns:
            G: a graph object
        """
        G = nx.Graph()
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    nodes = line.split()
                    for target in nodes[1:]:
                        G.add_edge(nodes[0], target)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{file_name}' was not found.")

        return G

    @staticmethod
    def read_digraph(file_name):
        """
        Reads a directed graph from a given file with edges having polynomial weights.

        Params:
            file_name: string
        Returns:
            G: a directed graph object
        """
        G = nx.DiGraph()
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    parts = line.split()
                    if len(parts) == 4:
                        source, target, a, b = parts
                        source, target = int(source), int(target)
                        G.add_edge(source, target, weight=(int(a), int(b)))
                    else:
                        print(f"Invalid line format: {line}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{file_name}' was not found.")

        return G

    @staticmethod
    def save_graph(G, file_name):
        """
        Saves a graph to a file.

        Params:
            G: graph object
            file_name: string
        """
        with open(file_name, 'w') as file:
            if G.is_directed():
                for source, target in G.edges():
                    a, b = G[source][target].get('weight', (0, 0))
                    line = f'{source} {target} {a} {b}\n'
                    file.write(line)
            else:
                for source in G.nodes():
                    targets = [str(target) for target in G.adj[source]]
                    line = f'{source} ' + ' '.join(targets) + '\n'
                    file.write(line)