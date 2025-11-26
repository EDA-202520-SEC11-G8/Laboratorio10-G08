from DataStructures.Map import map_linear_probing as mp
from DataStructures.Map import priority_queue as pq
from DataStructures.Stack import stack
from DataStructures.Graph import digraph as G
from DataStructures.Graph.dijsktra_structure import new_dijsktra_structure
import math


def dijkstra(my_graph, source):
    """
    Ejecuta el algoritmo de Dijkstra desde un vertice origen.
    Encuentra los caminos más cortos desde source a todos los demás vertices.
    """
    # Crear la estructura usando la función existente
    dijkstra_struct = new_dijsktra_structure(source, G.order(my_graph))
    
    # Insertar el origen con distancia 0
    mp.put(dijkstra_struct["visited"], source, {
        "dist_to": 0,
        "edge_to": None
    })
    pq.insert(dijkstra_struct["pq"], 0, source)
    
    # Mientras la cola de prioridad no esté vacía
    while not pq.is_empty(dijkstra_struct["pq"]):
        # Obtener el vértice con menor distancia
        min_vertex = pq.remove(dijkstra_struct["pq"])
        
        # Obtener la información del vértice
        vertex_info = mp.get(dijkstra_struct["visited"], min_vertex)
        dist_v = vertex_info["dist_to"]
        
        # Relajar los arcos adyacentes
        edges = G.edges_vertex(my_graph, min_vertex)
        i = 0
        while i < edges["size"]:
            edge = edges["elements"][i]
            w = edge["vertexB"]
            weight = edge["weight"]
            
            # Calcular nueva distancia
            new_dist = dist_v + weight
            
            # Verificar si w ya fue visitado
            w_info = mp.get(dijkstra_struct["visited"], w)
            
            if w_info is None:
                # Primera vez que visitamos w
                mp.put(dijkstra_struct["visited"], w, {
                    "dist_to": new_dist,
                    "edge_to": edge
                })
                pq.insert(dijkstra_struct["pq"], new_dist, w)
            else:
                if new_dist < w_info["dist_to"]:
                    # Encontramos un camino más corto a w
                    w_info["dist_to"] = new_dist
                    w_info["edge_to"] = edge
                    mp.put(dijkstra_struct["visited"], w, w_info)
                    # Mejorar prioridad en la cola
                    pq.improve_priority(dijkstra_struct["pq"], new_dist, w)
            
            i = i + 1
    
    return dijkstra_struct


def has_path_to(dijkstra_struct, vertex):
    """
    Retorna True si existe un camino desde el origen hasta vertex.
    """
    return mp.contains(dijkstra_struct["visited"], vertex)


def dist_to(dijkstra_struct, vertex):
    """
    Retorna la distancia más corta desde el origen hasta vertex.
    """
    vertex_info = mp.get(dijkstra_struct["visited"], vertex)
    if vertex_info is None:
        return math.inf
    return vertex_info["dist_to"]


def path_to(vertex, dijkstra_struct):
    """
    Retorna una pila con el camino más corto desde el origen hasta vertex.
    Cada elemento de la pila es un arco (edge).
    """
    # Si no hay camino, retornar None
    if not has_path_to(dijkstra_struct, vertex):
        return None

    # Crear pila vacia
    path = stack.new_stack()

    current = vertex
    source = dijkstra_struct["source"]
    
    # Reconstruir el camino desde vertex hasta source
    while current != source:
        vertex_info = mp.get(dijkstra_struct["visited"], current)
        edge = vertex_info["edge_to"]
        
        if edge is None:
            return None
        
        stack.push(path, edge)
        current = edge["vertexA"]

    return path