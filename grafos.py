import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox

nombre_cuidad="Lima, Peru" # Variable de ciudad a GRAFicar (xd)
G = ox.graph_from_place(nombre_cuidad, network_type='drive')

type(G)

ox.plot_graph(G, node_size=1, node_color='blue', edge_color='gray', bgcolor='white', show=True, save=False)