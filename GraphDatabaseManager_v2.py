""" Represents the database as a graph.
    Construct the graph database
    Utilities for viewing graphs and subgraphs.
    Utilities for performing projections.   

    Michael A. Goodrich
    Brigham Young University

    March 2023
"""
import networkx as nx
from matplotlib import pyplot as plt

from DatabaseManager import DatabaseManager
import numpy as np


class GraphManager:
    def __init__(self, file_name, directed_graph=False, node_types=[['country', 'age', 'sex'], ['suicides_per_100k_bins']]):
        self.database = DatabaseManager(file_name)
        self.node_types = node_types
        if directed_graph:
            self.G = nx.empty_graph(create_using=nx.DiGraph)
        else:
            self.G = nx.empty_graph()
        self.nodes_by_attribute_dict = dict()
        self.__initializeGraph()

    ############################################
    # Public Extraction and Projection Methods #
    ############################################
    def extractBipartiteGraph(self, category_1, category_2):
        edge_set = self.database.getEdges(category_1, category_2)
        H = self.__edgesetToSubgraph(edge_set)
        return H

    def extractProjectionGraph(self, categories, AdjacentCAS):
        """ Project out the movie to see relationships
            between other database categories
        """
        
        if AdjacentCAS:
            if categories is list:
                edge_set = self.__extractAdjacentCASEdges(categories)
            else:
                edge_set = self.__extractAdjacentCASEdges([categories])
        
        else:
            if categories is list:
                edge_set = self.__extractProjectionEdges(categories)
            else:
                edge_set = self.__extractProjectionEdges([categories])
        
        H = self.__edgesetToSubgraph(edge_set)
        return H

    @staticmethod
    def extractLargestComponent(subgraph):
        largest_cc = max(nx.connected_components(subgraph), key=len)
        subgraph = subgraph.subgraph(largest_cc).copy()
        return subgraph

    def getGraph_of_Database(self):
        return self.G

    def getColormap_by_Nodetype(self, G=None):
        """{'age','year','sex','country','suicides_per_100k_bins'}"""
        if G is None:
            G = self.G
        nodelist = list(G.nodes())
        colormap = ['y' for _ in nodelist]
        node_types = self.__get_node_types()

        for i in range(len(G.nodes())):
            node = nodelist[i]
            if len(node_types) > 0 and node in self.nodes_by_attribute_dict[node_types[0]]:
                colormap[i] = 'y'
            elif len(node_types) > 1 and node in self.nodes_by_attribute_dict[node_types[1]]:
                colormap[i] = 'm'
            elif len(node_types) > 2 and node in self.nodes_by_attribute_dict[node_types[2]]:
                colormap[i] = 'g'
            elif len(node_types) > 3 and node in self.nodes_by_attribute_dict[node_types[3]]:
                colormap[i] = 'c'
            elif len(node_types) > 4 and node in self.nodes_by_attribute_dict[node_types[4]]:
                colormap[i] = 'b'
            elif len(node_types) > 5 and node in self.nodes_by_attribute_dict[node_types[5]]:
                colormap[i] = 'r'
            elif len(node_types) > 6 and node in self.nodes_by_attribute_dict[node_types[6]]:
                colormap[i] = 'k'
        return colormap

    ##################################
    # Miscellaneous Public Utilities #
    ##################################
    def exportToGephi(self, gephi_filename):
        # nx.write_gexf(G,gephi_filename)
        nx.write_gexf(self.G, "figures/SuicideRiskGraph.gexf")

    @staticmethod
    def exportSubgraphToGephi(H, gephi_filename):
        # nx.write_gexf(G,gephi_filename)
        nx.write_gexf(H, "figures/SuicideRiskGraph_Subgraph.gexf")

    ##########################
    # Private Helper Methods #
    ##########################
    # Modified in version 2 by Jonathan
    def __initializeGraph(self):
        # Step 1: Create graph nodes based on self.node_types
        for categories in self.node_types:
            node_sets = []
            for category in categories:
                node_sets += [self.database.getNodesOfType(category)]

            concat = set(np.array(list(node_sets[0]), dtype=str))  # initialize and make every category a string
            for i in range(1, len(node_sets)):
                original_concat = concat.copy()
                concat = []
                for node in original_concat:
                    for node2 in node_sets[i]:
                        concat += [str(node) + ', ' + str(node2)]
            concat = set(concat)
            self.__addNodes(concat, categories)

        # Step 2: Initialize edge set
        for index, row in self.database.dataframe.iterrows():
            nodes = []
            for categories in self.node_types:
                cat = ''
                for category in categories:
                    cat += str(row[category]) + ', '
                nodes += [cat[:-2]]
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    # add to weighted edge if edge already exists!
                    if self.G.has_edge(nodes[i], nodes[j]):
                        self.G.add_weighted_edges_from([(nodes[i], nodes[j], self.G.get_edge_data(nodes[i], nodes[j])['weight'] + 1)])
                    else:
                        self.G.add_weighted_edges_from([(nodes[i], nodes[j], 1)])

    def __addNodes(self, node_set, categories):
        cat_type = self.__get_node_type(categories)
        self.G.add_nodes_from(node_set)
        self.nodes_by_attribute_dict[cat_type] = node_set

    def __addEdges(self, edge_set):
        self.G.add_edges_from(edge_set)

    @staticmethod
    def __edgesetToSubgraph(edge_set):
        H = nx.empty_graph()
        for edge in edge_set:
            H.add_edge(edge[0], edge[1])
        return H

    def __extractProjectionEdges(self, categories):
        """ Project out the movie to see relationships
            between other database categories
        """
        # The projections are performed by finding all paths two steps or fewer
        two_step_paths = dict(nx.all_pairs_shortest_path_length(self.G, cutoff=2))
        node_set = set()
        # Extract all the node types of interest
        for node_type in categories:
            node_set = node_set.union(self.nodes_by_attribute_dict[node_type])
        # Select only two-step paths between nodes of interest
        edge_set = set()
        for node_source in node_set:
            destination_dictionary = two_step_paths[node_source]
            node_destinations = set([k for k, v in destination_dictionary.items() if v == 2])
            node_destinations = node_destinations.intersection(node_set)
            for node_destination in node_destinations:
                edge_set.add((node_source, node_destination))
        return edge_set
    
    def __extractAdjacentCASEdges(self, categories):
    # Create sorted bins for each node based on category
        bins = {}
        for category in categories:
            node_list = list(self.nodes_by_attribute_dict[category])
            node_list.sort()
            bins[category] = node_list

        # Create a graph and add nodes to it
        H = nx.Graph()
        for node in self.G.nodes:
            if node in node_list:
                H.add_node(node)

        # Add edges between nodes belonging to adjacent bins
        for category in bins:
            node_list = bins[category]
            for i, node in enumerate(node_list):
                if i > 0:
                    H.add_edge(node, node_list[i-1])
                if i < len(node_list)-1:
                    H.add_edge(node, node_list[i+1])

        return H.edges()

    @staticmethod
    def __get_node_type(categories):
        cat = ''
        for category in categories:
            cat += str(category) + ', '
        return cat[:-2]

    def __get_node_types(self):
        cat_types = []
        for categories in self.node_types:
            cat_types += [self.__get_node_type(categories)]
        return cat_types

