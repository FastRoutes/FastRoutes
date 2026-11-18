# FastRoutes
Data Structures Final Project - 4th Semester - Software Engineering at Universidad Nacional Mayor de San Marcos

Calcula la ruta de reparto más corta (en tiempo) que sale del negocio, pasa por todas las entregas y regresa al negocio, respetando el sentido de las calles.

## Flujo de trabajo
1. **Nodos en el mapa de calles**: el negocio y las entregas elegidas se ajustan al nodo de calle más cercano (grafo dirigido de OpenStreetMap).
2. **Dijkstra**: desde cada nodo seleccionado se hallan los caminos mínimos hacia todos los demás nodos seleccionados.
3. **Grafo artificial**: los nodos seleccionados forman un grafo completo dirigido cuyas aristas son esos caminos mínimos (peso = tiempo de viaje). Es asimétrico por las calles de un solo sentido. Aquí se resuelve el TSP.
4. **Greedy (aproximación)**: solución inicial rápida del TSP asimétrico. Acepta los arcos de menor a mayor costo evitando salidas/entradas repetidas y subciclos prematuros.
5. **Tour improvement con Or-opt**: mueve segmentos de 1 a 3 paradas a otra posición del tour sin invertirlos, por lo que es válido para TSP asimétrico (2-opt no lo es). Se repite hasta que ningún movimiento mejora.
6. **De vuelta al mapa real**: cada arista del tour final se reemplaza por su camino real de calles obtenido en Dijkstra y se dibuja sobre el mapa.

## Estructura
```
app.py · api.py · config.py     Servidor Flask, endpoints y reglas de negocio
servicios/                      Validaciones y caso de uso "calcular ruta" (orquesta los 6 pasos)
grafo/                          Descarga OSM, caché, modelo del grafo dirigido de calles
algoritmos/
    dijkstra.py                 Caminos mínimos y reconstrucción de caminos
    grafo_artificial.py         Grafo artificial (puntos + caminos mínimos) y traslado al mapa real
    greedy.py                   Greedy (aproximación) para TSP asimétrico
    or_opt.py                   Or-opt (mejora del tour) para TSP asimétrico
    tsp.py                      Greedy + Or-opt
    costos.py                   Costo de un circuito
frontend/                       index.html + css/ + js/ (módulos ES)
tests/                          Pruebas unitarias e integración (unittest)
```

## Ejecutar
```
pip install -r requirements.txt
python app.py
```
Abrir http://localhost:5000

## Pruebas
```
python -m unittest discover -s tests -t .
```
