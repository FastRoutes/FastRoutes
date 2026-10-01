import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
from pyrosm import OSM

ruta_archivo = "peru-260930.osm.pbf" # Archivo OSM de Perú descargado desde Geofabrik

# Diccionario con los límites de las ciudades a elegir 
# Formato: [min_lon (Oeste), min_lat (Sur), max_lon (Este), max_lat (Norte)]
ciudades_peru = {
    "Lima": [-77.15, -12.15, -76.90, -11.90],
    "Arequipa": [-71.58, -16.44, -71.48, -16.36],
    "Cusco": [-71.99, -13.54, -71.94, -13.50]
}

ciudad_seleccionada = "Lima" # Variable de ciudad a GRAFicar (xd)
limites = ciudades_peru[ciudad_seleccionada]

# Inicialización de Pyrosm acotando la extracción exclusivamente a la ciudad elegida
osm_ciudad = OSM(ruta_archivo, bounding_box=limites)

# Extracción de los nodos y aristas de la red vial para vehículos
nodos, aristas = osm_ciudad.get_network(network_type="driving", nodes=True)

# Conversión de los datos a un grafo direccional NetworkX
G = osm_ciudad.to_graph(nodos, aristas, graph_type="networkx", direction="oneway")

# Preparación de los nodos de origen y destino (nodos aleatorios como ejemplo)
lista_nodos = list(G.nodes)
nodo_origen = lista_nodos[0]
nodo_destino = lista_nodos[100]

# Ejecución el Algoritmo de Dijkstra
# Pyrosm asigna automáticamente el peso 'length' (longitud en metros) a las aristas
ruta_optima = nx.dijkstra_path(G, source=nodo_origen, target=nodo_destino, weight='length')
distancia_total = nx.dijkstra_path_length(G, source=nodo_origen, target=nodo_destino, weight='length')

print(f"Ruta óptima calculada en {ciudad_seleccionada}: {len(ruta_optima)} nodos recorridos.")
print(f"Distancia de viaje: {distancia_total:.2f} metros.")

# Conversión a MultiDiGraph (OSMnx requiere este formato exacto para dibujar)
G_multi = nx.MultiDiGraph(G)

# Configuración y dibujo del mapa con la ruta superpuesta
# node_size=0 oculta los puntos para que se vean solo las calles
# route_color='red' resalta la ruta de Dijkstra
fig, ax = ox.plot_graph_route(
    G_multi, 
    ruta_optima, 
    route_color='red', 
    route_linewidth=4, 
    node_size=0, 
    bgcolor='white', 
    show=False, 
    close=False
)

# Exportar el gráfico como imagen en la misma carpeta del proyecto
nombre_imagen = f"mapa_ruta_{ciudad_seleccionada.lower()}.png"
plt.savefig(nombre_imagen, dpi=300, bbox_inches='tight')
print(f"Gráfico exportado exitosamente como '{nombre_imagen}'")

# Liberar memoria cerrando la figura internamente
plt.close(fig)