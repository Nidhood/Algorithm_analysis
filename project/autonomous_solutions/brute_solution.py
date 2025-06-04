#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
from copy import deepcopy
from free_flow.graph.graph import Graph
from free_flow.board.print_board import print_board
from utils.clear_screen import clear_screen


# -------------------------------------------------------------------------
# brute_solution :  Solucion de fuerza bruta para el juego Free Flow.
#                   Explora exhaustivamente todas las posibles combinaciones
#                   de caminos hasta encontrar una solucion valida.
# @inputs   :   Un grafo, objeto que representa el grafo del tablero del juego.
# @outputs  :   Valor booleano que indica si se encontro una solucion.
# @author   :   Ivan Dario Orozco Ibanez
# -------------------------------------------------------------------------
def brute_solution(graph: Graph):
    start_time = time.time() * 1000  # Tiempo en milisegundos

    print("Iniciando búsqueda exhaustiva...")
    print("Este proceso puede tomar mucho tiempo para tableros grandes.")
    print_board(graph)

    # Obtener todos los colores (pares de puntos) que necesitan conectarse
    colors = list(graph.initial_positions.keys())

    # Crear una copia del grafo para trabajar
    working_graph = deepcopy(graph)

    # Contador de intentos para mostrar progreso
    attempt_count = [0]

    # Llamar a la función recursiva de backtracking
    if solve_recursive(working_graph, colors, 0, attempt_count, start_time):
        # Copiar la solución encontrada al grafo original
        graph.matrix = working_graph.matrix
        graph.paths = working_graph.paths
        graph.connected_paths = working_graph.connected_paths
        graph.finished = True

        current_time = time.time() * 1000
        clear_screen()
        print("¡SOLUCIÓN ENCONTRADA CON FUERZA BRUTA!")
        print(f"Tiempo total: {current_time - start_time:.2f} ms")
        print(f"Intentos realizados: {attempt_count[0]}")
        print(f"Colores conectados: {len(colors)}")
        print_board(graph)
        return True
    else:
        current_time = time.time() * 1000
        print(f"\nNo se encontró solución después de {attempt_count[0]} intentos.")
        print(f"Tiempo transcurrido: {current_time - start_time:.2f} ms")
        return False


def solve_recursive(graph, colors, color_index, attempt_count, start_time):
    """
    Función recursiva que implementa backtracking para encontrar todos los caminos.

    @param graph: El grafo de trabajo
    @param colors: Lista de colores a conectar
    @param color_index: Índice del color actual en la lista
    @param attempt_count: Contador de intentos (lista para modificar por referencia)
    @param start_time: Tiempo de inicio para mostrar progreso
    @return: True si encuentra una solución válida, False en caso contrario
    """

    # Mostrar progreso cada cierto número de intentos
    attempt_count[0] += 1
    if attempt_count[0] % 1000 == 0:
        current_time = time.time() * 1000
        elapsed = current_time - start_time
        print(f"Intentos: {attempt_count[0]}, Tiempo: {elapsed:.2f} ms, Color actual: {color_index}/{len(colors)}")

    # Caso base: si hemos conectado todos los colores
    if color_index >= len(colors):
        # Verificar si el tablero está completamente lleno
        if is_board_full(graph):
            return True
        else:
            return False

    # Obtener el color actual
    current_color = colors[color_index]
    start_point, end_point = graph.initial_positions[current_color]

    # Generar todos los posibles caminos para este color
    all_paths = generate_all_paths(graph, current_color, start_point, end_point)

    # Probar cada camino posible
    for path in all_paths:
        # Crear una copia del estado actual del grafo
        saved_matrix = [row[:] for row in graph.matrix]

        # Aplicar el camino actual
        if apply_path_to_graph(graph, current_color, path):
            # Recursivamente intentar conectar el siguiente color
            if solve_recursive(graph, colors, color_index + 1, attempt_count, start_time):
                return True

            # Si no funcionó, restaurar el estado del grafo (backtrack)
            graph.matrix = saved_matrix
            if current_color in graph.paths:
                graph.paths[current_color] = [start_point, end_point]
            if current_color in graph.connected_paths:
                graph.connected_paths.remove(current_color)

    return False


def generate_all_paths(graph, color, start, end):
    """
    Genera todos los posibles caminos válidos entre dos puntos.

    @param graph: El grafo de trabajo
    @param color: El color/valor del camino
    @param start: Punto de inicio
    @param end: Punto final
    @return: Lista de todos los caminos válidos
    """
    all_paths = []
    max_path_length = graph.n * graph.m  # Longitud máxima razonable

    # Usar DFS para encontrar todos los caminos posibles
    def dfs_all_paths(current_path, visited):
        current_pos = current_path[-1]

        # Si llegamos al destino, agregar el camino
        if current_pos == end:
            all_paths.append(current_path[:])
            return

        # Si el camino es demasiado largo, podar
        if len(current_path) >= max_path_length:
            return

        # Explorar todos los vecinos
        for neighbor in get_valid_neighbors(graph, current_pos, color, end, visited):
            if neighbor not in visited:
                visited.add(neighbor)
                current_path.append(neighbor)
                dfs_all_paths(current_path, visited)
                current_path.pop()
                visited.remove(neighbor)

    # Iniciar la búsqueda desde el punto de inicio
    initial_visited = {start}
    dfs_all_paths([start], initial_visited)

    # Ordenar los caminos por longitud (preferir caminos más cortos primero)
    all_paths.sort(key=len)

    return all_paths


def get_valid_neighbors(graph, pos, color, end_point, visited):
    """
    Obtiene los vecinos válidos para el algoritmo de fuerza bruta.

    @param graph: El grafo de trabajo
    @param pos: Posición actual
    @param color: Color del camino actual
    @param end_point: Punto final del camino
    @param visited: Conjunto de posiciones ya visitadas
    @return: Lista de vecinos válidos
    """
    neighbors = []
    i, j = pos

    # Direcciones: arriba, abajo, izquierda, derecha
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for di, dj in directions:
        ni, nj = i + di, j + dj

        # Verificar límites del tablero
        if 0 <= ni < graph.n and 0 <= nj < graph.m:
            cell_value = graph.matrix[ni][nj]
            neighbor_pos = (ni, nj)

            # Condiciones para que sea un vecino válido:
            # 1. La celda está vacía (valor 0)
            # 2. Es el punto final del camino actual
            # 3. No ha sido visitada en el camino actual
            if ((cell_value == 0 or neighbor_pos == end_point) and
                    neighbor_pos not in visited):
                neighbors.append(neighbor_pos)

    return neighbors


def apply_path_to_graph(graph, color, path):
    """
    Aplica un camino al grafo y actualiza las estructuras de datos.

    @param graph: El grafo de trabajo
    @param color: Color del camino
    @param path: Lista de coordenadas que forman el camino
    @return: True si se aplicó correctamente, False en caso contrario
    """
    if len(path) < 2:
        return False

    start_point, end_point = graph.initial_positions[color]

    # Verificar que el camino comience y termine en los puntos correctos
    if path[0] != start_point or path[-1] != end_point:
        return False

    # Verificar que el camino sea continuo (celdas adyacentes)
    for i in range(len(path) - 1):
        curr = path[i]
        next_pos = path[i + 1]
        if not are_adjacent(curr, next_pos):
            return False

    # Aplicar el camino al grafo (sin sobrescribir los puntos inicial y final)
    for pos in path[1:-1]:  # Excluir puntos inicial y final
        row, col = pos
        if graph.matrix[row][col] != 0:  # La celda ya está ocupada
            return False
        graph.matrix[row][col] = color

    # Actualizar las estructuras de datos del grafo
    graph.paths[color] = path[:]
    graph.connected_paths.add(color)

    return True


def are_adjacent(pos1, pos2):
    """
    Verifica si dos posiciones son adyacentes (ortogonalmente).

    @param pos1: Primera posición (i, j)
    @param pos2: Segunda posición (i, j)
    @return: True si son adyacentes, False en caso contrario
    """
    i1, j1 = pos1
    i2, j2 = pos2
    return abs(i1 - i2) + abs(j1 - j2) == 1


def is_board_full(graph):
    """
    Verifica si el tablero está completamente lleno (no hay celdas con valor 0).

    @param graph: El grafo a verificar
    @return: True si está lleno, False en caso contrario
    """
    for i in range(graph.n):
        for j in range(graph.m):
            if graph.matrix[i][j] == 0:
                return False
    return True