from DataStructures.Map import map_functions as mf
import DataStructures.Map.map_linear_probing as mlp

from DataStructures.Graph import vertex as vtx


def new_graph(order):
    graph = {
        "vertices": mlp.new_map(order, 0.5),  # load_factor = 0.5 como en el ejemplo
        "num_edges": 0
    }

    return graph

def insert_vertex(my_graph, key_u, info_u):
    pass
def add_edge(my_graph, key_u, key_v, weight=1.0):
    pass


def contains_vertex():
    pass

def order():
    pass

def size():
    pass

