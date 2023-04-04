# Run.py. Place that Mike uses to experiment with code.

def main():
    # Exercise the necessary parts of the Database manager
    from DatabaseManager import DatabaseManager # I don't know if it's good form to do this or not
    database = DatabaseManager('datasets/suicide_rates_by_category.csv')
    database.printDatabaseOverview()
    database.showUniqueNodesOfType('generation')
    database.cleanDatabase()
    database.showUniqueNodesOfType('generation')
    database.binCategory('suicides_per_100k',binlist = [0,25,75,100,125,150,300])
    database.showUniqueNodesOfType('suicides_per_100k_bins')
    del database

    # Extract a knowledge graph
    from GraphDatabaseManager import GraphManager
    import networkx as nx
    from matplotlib import pyplot as plt

    #graph_database = GraphManager('datasets/suicide_rates_by_category.csv')
    #node_list = graph_database.getGraph_of_Database()
    #G = nx.Graph()
    #G.add_nodes_from(node_list)

main()