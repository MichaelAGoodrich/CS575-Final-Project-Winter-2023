import pandas as pd
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

class GraphAnalytics:
    def __init__(self, largestComponent):
        self.G = largestComponent

    def getGraphAnalysis(self):
        avg_degree = self.G.number_of_edges() / self.G.number_of_nodes()
        print("avg degree: ", avg_degree)

        print("assortativity coefficient: ", nx.degree_assortativity_coefficient(self.G))

        #print("diameter: ", nx.diameter(self.G))
        #print("radius: ", nx.radius(self.G))

    def showCommunities(self):
        pos = nx.nx_agraph.graphviz_layout(self.G, prog='neato')
        partition = nx.community.louvain_communities(self.G, weight='weight', seed=1)
        num_partitions = len(partition)

        color_map = self.getColormap_by_Louvain_Communities(partition)

        # Plot figure of largest component - same as above I just wanted you to visually see what graph we are working with
        plt.figure(1)
        nx.draw_networkx(self.G, pos, node_color=color_map, alpha=0.8, node_size=40, with_labels=False)
        ax = plt.gca()
        age_line, = ax.plot(-np.inf, -np.inf, 'y.', markersize=10)
        #age_line.set_label('Country, Age, Sex')
        year_line, = ax.plot(-np.inf, -np.inf, 'm.', markersize=10)
        #year_line.set_label('Suicide Bin')
        ax.legend()
        plt.show()

    def getColormap_by_Louvain_Communities(self, partition):
        nodelist = list(self.G.nodes())
        self.colormap = ['y' for _ in nodelist]
        num_partitions = len(partition)
        #find which partition the node is in, and then make it that color
        for i in range(0, num_partitions):
            for j in range(0, len(nodelist)):
                node = nodelist[j]
                if partition[i].__contains__(node):
                    if i == 0:
                        self.colormap[j] = 'y'
                    elif i == 1:
                        self.colormap[j] = 'm'
                    elif i == 2:
                        self.colormap[j] = 'g'
                    elif i == 3:
                        self.colormap[j] = 'c'
                    elif i == 4:
                        self.colormap[j] = 'b'
                    elif i == 5:
                        self.colormap[j] = 'r'
                    else:
                        self.colormap[j] = 'k'
        return self.colormap