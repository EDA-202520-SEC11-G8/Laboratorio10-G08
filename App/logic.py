"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

# ___________________________________________________
#  Importaciones
# ___________________________________________________

from DataStructures.List import single_linked_list as lt
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as m
from DataStructures.Stack import stack as st
from DataStructures.Graph import digraph as G
from DataStructures.Graph import dfs as DFS
from DataStructures.Graph import bfs as BFS
from DataStructures.Graph import dijsktra as DIJKSTRA

import csv
import time
import os
import math

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = new_analyzer()
    return analyzer


def new_analyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar la información de las paradas
   connections: Grafo para representar las rutas entre estaciones
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
            'stops': None,
            'connections': None,
            'paths': None
        }

        analyzer['stops'] = m.new_map(
            num_elements=8000, load_factor=0.7, prime=109345121)

        analyzer['connections'] = G.new_graph(order=20000)
        return analyzer
    except Exception as exp:
        return exp

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def load_services(analyzer, servicesfile, stopsfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    stopsfile = data_dir + stopsfile
    stops_input_file = csv.DictReader(open(stopsfile, encoding="utf-8"),
                                      delimiter=",")

    for stop in stops_input_file:
        add_stop(analyzer, stop)

    servicesfile = data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    for service in input_file:
        if not G.contains_vertex(analyzer['connections'], format_vertex(service)):
            add_stop_vertex(analyzer, format_vertex(service))
        add_route_stop(analyzer, service)

        if lastservice is not None:
            sameservice = lastservice['ServiceNo'] == service['ServiceNo']
            samedirection = lastservice['Direction'] == service['Direction']
            samebusStop = lastservice['BusStopCode'] == service['BusStopCode']
            if sameservice and samedirection and not samebusStop:
                add_stop_connection(analyzer, lastservice, service)

        add_same_stop_connections(analyzer, service)
        lastservice = service

    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def total_stops(analyzer):
    """
    Total de paradas de autobus en el grafo.
    """
    return G.order(analyzer['connections'])



def total_connections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return G.size(analyzer['connections'])


# Funciones para la medición de tiempos

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para agregar informacion al grafo

def add_stop_connection(analyzer, lastservice, service):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = format_vertex(lastservice)
        destination = format_vertex(service)
        clean_service_distance(lastservice, service)
        distance = float(service['Distance']) - float(lastservice['Distance'])
        distance = abs(distance)
        add_connection(analyzer, origin, destination, distance)
        return analyzer
    except Exception as exp:
        return exp


def add_stop(analyzer, stop):
    """
    Adiciona una parada (BusStopCode) en los stops del sistema de transporte
    """
    stop['services'] = lt.new_list()
    m.put(analyzer['stops'], stop['BusStopCode'], stop)
    return analyzer

def add_stop_vertex(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """

    G.insert_vertex(analyzer['connections'], stopid, stopid)
    return analyzer


def add_route_stop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    stop_info = m.get(analyzer['stops'], service['BusStopCode'])
    stop_services = stop_info['services']
    if lt.is_present(stop_services, service['ServiceNo'], lt.default_function) == -1:
        lt.add_last(stop_services, service['ServiceNo'])

    return analyzer


def add_connection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """

    G.add_edge(analyzer['connections'], origin, destination, distance)



def add_same_stop_connections(analyzer, service):
    stop_1 = format_vertex(service)
    stop_buses_lt = m.get(analyzer['stops'], service['BusStopCode'])['services']

    if lt.size(stop_buses_lt) > 1:
        pass

    node = stop_buses_lt['first']
    for _ in range(lt.size(stop_buses_lt)):
        stop_2 = format_vertex({'BusStopCode': service['BusStopCode'], 'ServiceNo': node['info']})
        if stop_1 != stop_2:
            add_connection(analyzer, stop_1, stop_2, 0)
        node = node['next']
    return analyzer


# ___________________________________________________
#  Funciones de resolución de requerimientos
# ___________________________________________________

def get_most_concurrent_stops(analyzer):
    """
    Obtiene las 5 paradas más concurridas
    """
    graph = analyzer["connections"]
    verts = G.vertices(graph)
    resultados = lt.new_list()
    
    for i in range(m.size(verts)):
        key = verts["elements"][i]
        deg = G.degree(graph, key)
        
        lt.add_last(resultados, (key, deg))
    def compare(e1, e2):
        return e1[1] > e2[1]
    resultados = lt.merge_sort(resultados, compare)
    
    top5 = al.new_list()

    limite = min(5, lt.size(resultados))

    for i in range(limite):
        al.add_last(top5, lt.get_element(resultados, i))
        
    return top5
        
    

def get_route_between_stops_dfs(analyzer, stop1, stop2):
    """
    Obtener la ruta entre dos paradas usando DFS.
    """

    # ejecutar DFS desde la parada origen
    dfo = DFS.dfs(analyzer["connections"], stop1)

    # verificar si hay camino
    if not DFS.has_path_to(stop2, dfo):
        return None

    # obtener el camino
    path_stack = DFS.path_to(stop2, dfo)

    # convertir la pila
    ruta = []
    while not st.is_empty(path_stack):
        ruta.append(st.pop(path_stack))

    return ruta

def get_route_between_stops_bfs(analyzer, stop1, stop2):
    """
    Obtener la ruta entre dos paradas usando BFS.
    """
    # Ejecutar BFS desde la parada origen
    bfo = BFS.bfs(analyzer["connections"], stop1)

    # Verificar si hay camino
    if not BFS.has_path_to(stop2, bfo):
        return None

    # Obtener el camino
    path_stack = BFS.path_to(stop2, bfo)

    # Convertir la pila a array_list
    ruta = al.new_list()
    while not st.is_empty(path_stack):
        elemento = st.pop(path_stack)
        al.add_first(ruta, elemento)

    return ruta

def get_shortest_route_between_stops(analyzer, stop1, stop2):
    """
    Obtener la ruta mínima entre dos paradas.
    
    Nota: Se guarda en analyzer['paths'] el resultado del algoritmo de Dijkstra
    """
    # Ejecutar Dijkstra desde la parada origen
    analyzer['paths'] = DIJKSTRA.dijkstra(analyzer["connections"], stop1)
    # Verificar si hay camino
    if not DIJKSTRA.has_path_to(stop2, analyzer['paths']):
        return None

    # Obtener el camino
    path_stack = DIJKSTRA.path_to(stop2, analyzer['paths'])

    # Obtener la distancia total
    distance = DIJKSTRA.dist_to(stop2, analyzer['paths'])

    # Convertir la pila
    ruta = []
    while not st.is_empty(path_stack):
        edge = st.pop(path_stack)
        ruta.append(edge)

    return ruta[::-1], distance

def show_calculated_shortest_route(analyzer, destination_stop):
    # (Opcional) TODO: Mostrar en un mapa la ruta mínima entre dos paradas usando folium
    ...




# ___________________________________________________
# Funciones Helper
# ___________________________________________________

def clean_service_distance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def format_vertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name
