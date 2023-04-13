# Run.py. Place that Mike uses to experiment with code.

def main():
    # Exercise the necessary parts of the Database manager
    from DatabaseManager import DatabaseManager  # I don't know if it's good form to do this or not
    database = DatabaseManager('datasets/suicide_rates_by_category.csv')
    database.showUniqueNodesOfType('generation')
    database.cleanDatabase()
    database.showUniqueNodesOfType('generation')
    database.binCategory('suicides_per_100k', binlist=[0, 25, 75, 100, 125, 150, 300])
    database.showUniqueNodesOfType('suicides_per_100k_bins')
    database.printDatabaseOverview()
    del database

    # Extract a knowledge graph
    from GraphDatabaseManager import GraphManager
    import networkx as nx
    from matplotlib import pyplot as plt
    import numpy as np

    graph_database = GraphManager('datasets/suicide_rates_by_category.csv')
    G = graph_database.getGraph_of_Database()
    pos = nx.nx_agraph.graphviz_layout(G, prog='neato')
    color_map = graph_database.getColormap_by_Nodetype()
    plt.figure(1)
    nx.draw_networkx(G, pos, node_color=color_map, alpha=0.8, node_size=40, with_labels=False)
    ax = plt.gca()
    age_line, = ax.plot(-np.inf, -np.inf, 'y.', markersize=10)
    age_line.set_label('age')
    year_line, = ax.plot(-np.inf, -np.inf, 'm.', markersize=10)
    year_line.set_label('year')
    sex_line, = ax.plot(-np.inf, -np.inf, 'g.', markersize=10)
    sex_line.set_label('sex')
    country_line, = ax.plot(-np.inf, -np.inf, 'c.', markersize=10)
    country_line.set_label('country')
    rate_line, = ax.plot(-np.inf, -np.inf, 'b.', markersize=10)
    rate_line.set_label('suicide bin')
    ax.legend()
    plt.show()


main()
