#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#

import itertools
import numpy as np
import networkx as nx

def chinese_postman(graph,starting_node=None,verbose=False):
	
	def get_shortest_distance(graph, pairs, edge_weight_name):
		return {pair : nx.dijkstra_path_length(graph, pair[0], pair[1], edge_weight_name) for pair in pairs}
	
	def create_graph(node_pairs_with_weights, flip_weight = True):
		graph = nx.Graph()
		for k,v in node_pairs_with_weights.items():
			wt = -v if flip_weight else v
			graph.add_edge(k[0], k[1], **{'distance': v, 'weight': wt})
		return graph
	
	def create_new_graph(graph, edges, starting_node=None):
		g = nx.MultiGraph()
		for edge in edges:
			aug_path  = nx.shortest_path(graph, edge[0], edge[1], weight="distance")
			aug_path_pairs  = list(zip(aug_path[:-1],aug_path[1:]))
			
			for aug_edge in aug_path_pairs:
				aug_edge_attr = graph[aug_edge[0]][aug_edge[1]]
				g.add_edge(aug_edge[0], aug_edge[1], attr_dict=aug_edge_attr)
		for edge in graph.edges(data=True):
			g.add_edge(edge[0],edge[1],attr_dict=edge[2:])
		return g
	
	def create_eulerian_circuit(graph, starting_node=starting_node):
		return list(nx.eulerian_circuit(graph,source=starting_node))
	
	odd_degree_nodes = [node for node, degree in dict(nx.degree(graph)).items() if degree%2 == 1]
	odd_degree_pairs = itertools.combinations(odd_degree_nodes, 2)
	odd_nodes_pairs_shortest_path = get_shortest_distance(graph, odd_degree_pairs, "distance")
	graph_complete_odd = create_graph(odd_nodes_pairs_shortest_path, flip_weight=True)
	if verbose:
		print('Number of nodes (odd): {}'.format(len(graph_complete_odd.nodes())))
		print('Number of edges (odd): {}'.format(len(graph_complete_odd.edges())))
	odd_matching_edges = nx.algorithms.max_weight_matching(graph_complete_odd, True)
	if verbose: print('Number of edges in matching: {}'.format(len(odd_matching_edges)))
	multi_graph = create_new_graph(graph, odd_matching_edges)
	
	return(create_eulerian_circuit(multi_graph, starting_node))