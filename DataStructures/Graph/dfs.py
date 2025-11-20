from DataStructures.Map import map_linear_probing as map
from DataStructures.Queue import queue
from DataStructures.Stack import stack
from DataStructures.Graph.dfo_structure import new_dfo_structure
from DataStructures.Graph import digraph as G



def dfs(my_graph, source):
    """
    Ejecuta DFS desde un vertice origen.
    Retorna la estructura dfo_structure.
    """

    # crear la estructura
    dfo = new_dfo_structure(G.order(my_graph))

    dfs_vertex(my_graph, source, dfo)

    return dfo



def dfs_vertex(my_graph, vertex, dfo):
    """
    Funcion recursiva para visitar vertices.
    """

    # marcar como visitado
    map.put(dfo["marked"], vertex, True)

    # agregar en preorden
    queue.enqueue(dfo["pre"], vertex)

    # recorrer los vecinos
    adjs = G.adjacents(my_graph, vertex)
    for w in adjs["elements"]:
        if not map.contains(dfo["marked"], w):
            dfs_vertex(my_graph, w, dfo)


    # agregar en postorden
    queue.enqueue(dfo["post"], vertex)

    # agregar en reverso postorden (para top sort)
    stack.push(dfo["reversepost"], vertex)
    
    
def has_path_to(vertex, dfo):
    """
    Retorna True si vertex fue visitado.
    """

    # si está marcado : hay camino
    return map.contains(dfo["marked"], vertex)


def path_to(vertex, dfo):
    """
    Retorna una pila con el camino desde el origen hasta vertex.
    """

    # si no hay camino → None
    if not has_path_to(vertex, dfo):
        return None

    # crear pila vacia
    path = stack.new_stack()
    node = dfo["reversepost"]["first"]

    while node is not None:
        v = node["info"]
        stack.push(path, v)
        if v == vertex:
            break
        node = node["next"]

    return path