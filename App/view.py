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


import sys
import threading
from App import logic

import DataStructures.List.array_list as lt
"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


servicefile = 'bus_routes_14000.csv'
stopsfile = 'bus_stops.csv'
initialStation = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def print_menu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Cargar información de buses de singapur") # Clase 1: Implementar digraph básico
    print("2- Encontrar las paradas más concurridas") # Casa 1: Implementar digraph completo
    print("3- Encontrar una ruta entre dos paradas (DFS)") # Casa 1: Implementar funcionalidad dfs
    print("4- Encontrar una ruta entre dos paradas (BFS)") # Clase 2: Implementar funcionalidad bfs
    print("5- Encontrar la ruta mínima entre dos paradas") # Casa 2: Implementar dijkstra
    print("6- Mostrar en un mapa la ruta mínima entre dos paradas") # Trabajo Complementario: Mostrar ruta con folium
    print("0- Salir")
    print("*******************************************")


def option_one(cont):
    print("\nCargando información de transporte de singapur ....")
    logic.load_services(cont, servicefile, stopsfile)
    numedges = logic.total_connections(cont)
    numvertex = logic.total_stops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))

def option_two(cont):
    print("\nBuscando las paradas más concurridas...\n")
    top = logic.get_most_concurrent_stops(cont)
    print("Top 5 paradas con más conexiones:\n")
    for i in range(lt.size(top)):
        elem = lt.get_element(top, i)
        stop_id, degree = elem
        print(f"- Parada: {stop_id}, conexiones salientes: {degree}")
    


def option_three(cont):
    print("Ingrese parada origen:")
    origin = input("> ")

    print("Ingrese parada destino:")
    destination = input("> ")

    ruta = logic.get_route_between_stops_dfs(cont, origin, destination)

    if ruta is None:
        print("No existe ruta entre las paradas.")
    else:
        print("Ruta encontrada (DFS):")
        
        imprimir_ruta_formateada(ruta)

def option_four(cont):
    print("Ingrese parada origen:")
    origin = input("> ")

    print("Ingrese parada destino:")
    destination = input("> ")

    ruta = logic.get_route_between_stops_bfs(cont, origin, destination)

    if ruta is None:
        print("No existe ruta entre las paradas.")
    else:
        print("Ruta encontrada (BFS):")
        # Convertir array_list de la lógica a lista normal:
        paradas = []
        for i in range(lt.size(ruta)):
            paradas.append(lt.get_element(ruta, i))

        imprimir_ruta_formateada(paradas)

def option_five(cont):
    print("Ingrese parada origen:")
    origin = input("> ")

    print("Ingrese parada destino:")
    destination = input("> ")

    resultado = logic.get_shortest_route_between_stops(cont, origin, destination)

    if resultado is None:
        print("No existe ruta mínima entre las paradas.")
        return

    ruta, distancia = resultado

    print(f"Ruta mínima encontrada (Dijkstra):")
    print(f"Distancia total: {distancia:.2f} km\n")

    # La ruta que retorna Dijkstra es una lista de arcos (tuplas u objetos)
    paradas = []
    for edge in ruta:
        # edge = (start, end, weight)  <-- típico formato en su implementación
        # Necesitamos extraer el nombre del vértice destino
        paradas.append(edge[1])

    imprimir_ruta_formateada(paradas)

def option_six(cont):
    # (Opcional) TODO: Imprimir los resultados de la opción 6
    ...

def imprimir_ruta_formateada(paradas):
    ruta_actual = []
    bus_actual = paradas[0].split("-")[1]
    parada_inicio = paradas[0].split("-")[0]
    
    print(f"--- Tomar el bus '{bus_actual}' desde '{parada_inicio}' ---")
    
    for bus_stop in paradas:
        bus = bus_stop.split("-")[1]
        parada = bus_stop.split("-")[0]
        if bus != bus_actual:
            # Imprimir ruta del bus anterior
            print(" > ".join(ruta_actual))
            last_parada = ruta_actual[-1]
            
            print(f"--- Cambiar el bus '{bus}' desde '{last_parada}' ---")

            # Reiniciar la ruta
            ruta_actual = []
            bus_actual = bus
        
        ruta_actual.append(parada)
    
    print(" > ".join(ruta_actual))
    

"""
Menu principal
"""


def main():
    working = True
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            cont = logic.new_analyzer()
            option_one(cont)
        elif int(inputs[0]) == 2:
            option_two(cont)
        elif int(inputs[0]) == 3:
            option_three(cont)
        elif int(inputs[0]) == 4:
            option_four(cont)
        elif int(inputs[0]) == 5:
            option_five(cont)
        elif int(inputs[0]) == 6:
            option_six(cont)
        else:
            working = False
            print("Saliendo...")
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=main)
    thread.start()
