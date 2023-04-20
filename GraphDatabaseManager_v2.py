from collections import OrderedDict
import csv


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

    def extractProjectionGraph(self, category, AdjacentCAS):
        """ Project out the movie to see relationships
            between other database categories
        """
        if AdjacentCAS:
            borderData = self.getBorderData('datasets/GEODATASOURCE-COUNTRY-BORDERS.CSV')
            edge_set = self.__extractAdjacentCASEdges(category, borderData)
            
        else:
            edge_set = self.__extractProjectionEdges(category)

        print("edgeset: ", edge_set)
        
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
    
    def getBorderData(self, filename):
        borders = {}

        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header row
            for row in reader:
                country_code, country_name, border_code, border_name = row
                if border_name:
                    if country_name not in borders:
                        borders[country_name] = set()
                    borders[country_name].add(border_name)
                    if border_name not in borders:
                        borders[border_name] = set()
                    borders[border_name].add(country_name)
        
        return borders

    
    def __extractAdjacentCASEdges(self, category, borders):
        # Create sorted bins for each node based on category
        bins = OrderedDict([
            ("5-14", set()),
            ("15-24", set()),
            ("25-34", set()),
            ("35-54", set()),
            ("55-74", set()),
            ("75+", set())
        ])
        node_list = list(self.nodes_by_attribute_dict[category])
        
        for node in node_list:
            age = node.split(", ")[1].split(" ")[0]
            bins[age].add(node)
        
        bins = [v for k, v in bins.items()]

        # Create a graph and add nodes to it
        H = nx.Graph()
        for node in self.G.nodes:
            if node in node_list:
                H.add_node(node)

        # Add edges between nodes belonging to adjacent bins or with neighboring countries
        for node in node_list:
            country = node.split(",")[0]
            for i, bin in enumerate(bins):
                if node in bin:
                    break
            if i > 0:
                if country in borders:
                    for adj_node in bins[i-1]:
                        adj_country = adj_node.split(",")[0] 
                        if adj_country in borders[country]:
                            H.add_edge(node, adj_node)
            if i < len(bins)-1:
                if country in borders:
                    for adj_node in bins[i+1]:
                        adj_country = adj_node.split(",")[0] 
                        if adj_country in borders[country]:
                            H.add_edge(node, adj_node)
            
            if country in borders:
                for adj_node in bins[i]:
                    if not adj_node==node:
                        adj_country = adj_node.split(",")[0] 
                        if adj_country in borders[country]:
                            H.add_edge(node, adj_node)

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