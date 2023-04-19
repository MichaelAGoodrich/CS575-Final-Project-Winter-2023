# Run_v2.py. Place that Jonathan uses to experiment with code.
from GraphDatabaseManager_v2 import GraphManager
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
from DatabaseManager import DatabaseManager


def main():
    # I am not sure if the part is doing anything
    # Exercise the necessary parts of the Database manager
    database = DatabaseManager('datasets/suicide_rates_by_category.csv')
    database.showUniqueNodesOfType('generation')
    database.cleanDatabase()
    database.showUniqueNodesOfType('generation')
    database.binCategory('suicides_per_100k', binlist=[0, 25, 75, 100, 125, 150, 300])
    database.showUniqueNodesOfType('suicides_per_100k_bins')
    database.printDatabaseOverview()
    del database

    # Extract a knowledge graph
    graph_database = GraphManager('datasets/suicide_rates_by_category.csv')
    G = graph_database.getGraph_of_Database()
    G = graph_database.extractLargestComponent(G)  # let's only worry about the largest component!
    pos = nx.nx_agraph.graphviz_layout(G, prog='neato')
    # I edited the following function to use any graph (ie the largest component) by default will use the whole graph
    color_map = graph_database.getColormap_by_Nodetype(G)

    # Plot figure of largest component
    plt.figure(1)
    nx.draw_networkx(G, pos, node_color=color_map, alpha=0.8, node_size=40, with_labels=False)
    ax = plt.gca()
    age_line, = ax.plot(-np.inf, -np.inf, 'y.', markersize=10)
    age_line.set_label('Country, Age, Sex')
    year_line, = ax.plot(-np.inf, -np.inf, 'm.', markersize=10)
    year_line.set_label('Suicide Bin')
    ax.legend()
    plt.show()

    H = graph_database.extractProjectionGraph('country, age, sex', False)
    H = graph_database.extractLargestComponent(H)  # let's only worry about the largest component!
    pos = nx.nx_agraph.graphviz_layout(H, prog='neato')
    # I edited the following function to use any graph (ie the largest component) by default will use the whole graph
    color_map = graph_database.getColormap_by_Nodetype(H)

    # Plot figure of largest component
    plt.figure(1)
    nx.draw_networkx(H, pos, node_color=color_map, alpha=0.8, node_size=40, with_labels=False)
    ax = plt.gca()
    age_line, = ax.plot(-np.inf, -np.inf, 'y.', markersize=10)
    age_line.set_label('Country, Age, Sex')
    year_line, = ax.plot(-np.inf, -np.inf, 'm.', markersize=10)
    year_line.set_label('Suicide Bin')
    ax.legend()
    plt.show()


main()
