import math
from DataStructures.Map import priority_queue as pq
from DataStructures.Graph import digraph as dg
from DataStructures.Map import map_linear_probing as map
from DataStructures.Stack import stack as stack
from DataStructures.Graph import dijsktra_structure as dijsktra_structure
from DataStructures.List import array_list as lt


def dijkstra(my_graph, source):
    """
    Ejecuta el algoritmo de Dijkstra desde un vertice origen.
    Encuentra los caminos más cortos desde source a todos los demás vertices.
    """
    search = dijsktra_structure.new_dijsktra_structure(source, dg.order(my_graph))
    visited = search["visited"]
    heap = search["pq"]

    vertices = dg.vertices(my_graph)

    for i in range(lt.size(vertices)):
        v = lt.get_element(vertices, i)
        map.put(visited, v, {
            "marked": False,
            "dist_to": math.inf,
            "edge_from": None
        })

    v_info = map.get(visited, source)
    v_info["dist_to"] = 0
    map.put(visited, source, v_info)

    pq.insert(heap, 0, source)

    while not pq.is_empty(heap):

        dist_u, u = pq.remove(heap)
        u_info = map.get(visited, u)

        if u_info["marked"]:
            continue

        u_info["marked"] = True
        map.put(visited, u, u_info)

        edges = dg.edges_vertex(my_graph, u)

        for i in range(edges["size"]):
            edge = edges["elements"][i]
            w = edge["vertexB"]
            weight = edge["weight"]

            w_info = map.get(visited, w)

            if w_info["marked"]:
                continue

            new_dist = u_info["dist_to"] + weight

            if new_dist < w_info["dist_to"]:
                w_info["dist_to"] = new_dist
                w_info["edge_from"] = edge
                map.put(visited, w, w_info)

                if pq.contains(heap, w):
                    pq.improve_priority(heap, new_dist, w)
                else:
                    pq.insert(heap, new_dist, w)

    return search


def has_path_to(search, vertex):
    v_info = map.get(search["visited"], vertex)
    return v_info is not None and v_info["dist_to"] < math.inf


def dist_to(search, vertex):
    v_info = map.get(search["visited"], vertex)
    return v_info["dist_to"]


def path_to(search, vertex):
    if not has_path_to(search, vertex):
        return None

    path = stack.new_stack()
    current = vertex
    source = search["source"]
    visited = search["visited"]

    while current != source:
        v_info = map.get(visited, current)
        edge = v_info["edge_from"]
        if edge is None:
            return None
        stack.push(path, edge)
        current = edge["vertexA"]

    return path
