# FastRoutes
Data Structures Final Project - 4th Semester - Software Engineering at Universidad Nacional Mayor de San Marcos

## Estructura
```
app.py · api.py · config.py     Servidor Flask, endpoints y reglas de negocio
servicios/                      Validaciones y caso de uso "calcular ruta"
grafo/                          Descarga OSM, caché, modelo del grafo dirigido
algoritmos/                     Dijkstra, Held-Karp, vecino más cercano, 2-opt
frontend/                       index.html + css/ + js/ (módulos ES)
```
Ejecutar: `pip install -r requirements.txt && python app.py` → http://localhost:5000
