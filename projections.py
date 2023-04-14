import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from GraphDatabaseManager import GraphManager


def extractProjectionGraph(G, categories, database):
    """Project out the movie to see relationships
    between other database categories
    """
    edge_set = __extractProjectionEdges(G, categories, database)
    H = __edgesetToSubgraph(edge_set)
    return H


def __edgesetToSubgraph(edge_set):
    H = nx.empty_graph()
    for edge in edge_set:
        H.add_edge(edge[0], edge[1])
    return H


def __extractProjectionEdges(G, categories, database):
    """Project out the movie to see relationships
    between other database categories
    """
    # The projections is performed by finding all paths two steps or fewer
    two_step_paths = dict(nx.all_pairs_shortest_path_length(G, cutoff=2))
    node_set = set()
    # Extract all the node types of interest
    for node_type in categories:
        node_set = node_set.union(database.getNodesOfType(node_type))
    # Select only two step paths between nodes of interest
    edge_set = set()
    for node_source in node_set:
        destination_dictionary = two_step_paths[node_source]
        node_destinations = set(
            [k for k, v in destination_dictionary.items() if v == 2]
        )
        node_destinations = node_destinations.intersection(node_set)
        for node_destination in node_destinations:
            edge_set.add((node_source, node_destination))
    return edge_set


def get_color_map(G, manager):
    """{'age','year','sex','country','suicides_per_100k_bins'}"""
    nodelist = list(G.nodes())
    colormap = list(range(len(nodelist)))
    for i in range(len(nodelist)):
        node = nodelist[i]
        if node in manager.nodes_by_attribute_dict["age"]:
            colormap[i] = "y"
        elif node in manager.nodes_by_attribute_dict["year"]:
            colormap[i] = "m"
        elif node in manager.nodes_by_attribute_dict["sex"]:
            colormap[i] = "g"
        elif node in manager.nodes_by_attribute_dict["country"]:
            colormap[i] = "c"
        elif node in manager.nodes_by_attribute_dict["suicides_per_100k_bins"]:
            colormap[i] = "b"
    return colormap


def draw(G, manager, with_labels=False, figname=None, show=True, is_bipartite=False):
    if is_bipartite:
        pos = nx.bipartite_layout(G, manager.nodes_by_attribute_dict["age"])
    else:
        pos = nx.nx_agraph.graphviz_layout(G, prog="neato")
    color_map = get_color_map(G, manager)
    plt.figure(1)
    nx.draw_networkx(
        G, pos, node_color=color_map, alpha=0.8, node_size=40, with_labels=with_labels
    )
    ax = plt.gca()
    (age_line,) = ax.plot(-np.inf, -np.inf, "y.", markersize=10)
    age_line.set_label("age")
    (year_line,) = ax.plot(-np.inf, -np.inf, "m.", markersize=10)
    year_line.set_label("year")
    (sex_line,) = ax.plot(-np.inf, -np.inf, "g.", markersize=10)
    sex_line.set_label("sex")
    (country_line,) = ax.plot(-np.inf, -np.inf, "c.", markersize=10)
    country_line.set_label("country")
    (rate_line,) = ax.plot(-np.inf, -np.inf, "b.", markersize=10)
    rate_line.set_label("suicide bin")
    ax.legend()
    figure = plt.gcf()
    figure.set_size_inches(15, 10)
    if figname:
        plt.savefig(figname)
    if show:
        plt.show()
    plt.close()


manager = GraphManager("datasets/suicide_rates_by_category.csv")

# age to risk bipartite
age_risk_bipartite = manager.extractBipartiteGraph("age", "suicides_per_100k_bins")
assert nx.is_bipartite(age_risk_bipartite)
draw(
    age_risk_bipartite,
    manager,
    with_labels=True,
    figname="figures/age_risk_bipartite.png",
    show=False,
    is_bipartite=True,
)

age_risk_projection = manager.extractProjectionGraph(["age", "suicides_per_100k_bins"])
draw(
    age_risk_projection,
    manager,
    with_labels=True,
    figname="figures/age_risk_projection.png",
    show=False,
)

# Just age
age_projection = manager.extractProjectionGraph(["age"])
draw(
    age_projection,
    manager,
    with_labels=True,
    figname="figures/age_projection.png",
    show=False,
)
# Just age bipartite
age_bipartite_projection = extractProjectionGraph(
    age_risk_bipartite, ["age"], manager.database
)
draw(
    age_bipartite_projection,
    manager,
    with_labels=True,
    figname="figures/age_bipartite_projection.png",
    show=False,
)
