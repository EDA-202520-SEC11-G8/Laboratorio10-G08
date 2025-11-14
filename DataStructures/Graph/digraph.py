from DataStructures.Map import map_functions as mf
import DataStructures.Map.map_linear_probing as mlp

from DataStructures.Graph import vertex as vtx


def new_graph(order):
    graph = {
        "vertices": mlp.new_map(order, 0.5),  # load_factor = 0.5 
        "num_edges": 0
    }

    return graph

def insert_vertex(my_graph, key_u, info_u):
    # Crear un nuevo vértice 
    new_v = vtx.new_vertex(key_u, info_u)

    # Insertar o reemplazar el vértice en el mapa
    my_graph["vertices"] = mlp.put(my_graph["vertices"], key_u, new_v)

    return my_graph


def add_edge(my_graph, key_u, key_v, weight=1.0):
    # Buscar el vertice u
    vertex_u = mlp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        # Error si no existe u
        raise Exception("El vertice u no existe")

    # Buscar el vertice v
    vertex_v = mlp.get(my_graph["vertices"], key_v)
    if vertex_v is None:
        # Error si no existe v
        raise Exception("El vertice v no existe")

    # Revisar si el arco ya existe
    # Si existe, get_edge devuelve un arco; si no, devuelve None
    existe = vtx.get_edge(vertex_u, key_v)

    # Agregar o reemplazar el arco
    vtx.add_adjacent(vertex_u, key_v, weight)

    # Si el arco no existía, aumentar el número de arcos
    if existe is None:
        my_graph["num_edges"] += 1

    return my_graph

def contains_vertex(my_graph, key_u):
    """
    Retorna True si el vertice con llave key_u existe en el grafo.
    """
    return mlp.contains(my_graph["vertices"], key_u)

def order(my_graph):
    """
    Retorna el número de vértices del grafo (orden).
    """
    return mlp.size(my_graph["vertices"])

def size(my_graph):
    """
    Retorna el número de aristas del grafo.
    """
    return my_graph["num_edges"]