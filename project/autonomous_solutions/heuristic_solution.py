#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import random
import heapq
from copy import deepcopy
from free_flow.graph.graph import Graph
from free_flow.board.print_board import print_board
from utils.clear_screen import clear_screen
#-------------------------------------------------------------------------
# heuristic_solution :  Solucion heuristica para el juego Free Flow, basada en A* con poda.
# @inputs   :   Un grafo, objeto que representa el grafo del tablero del juego.
# @outputs  :   Valor booleano que indica si se encontro una solucion.
# @author   :   Ivan Dario Orozco Ibanez
#-------------------------------------------------------------------------
def heuristic_solution(graph: Graph):
    start_time = time.time() * 1000  # Tiempo en milisegundos

    # Ordenar colores por distancia Manhattan entre sus puntos
    colors = sorted(graph.initial_positions.keys(),
                    key=lambda c: manhattan_distance(graph.initial_positions[c][0], graph.initial_positions[c][1]))

    # Intentar conectar los colores en orden
    for i, color in enumerate(colors):
        start, end = graph.initial_positions[color]
        if not connect_color(graph, color, start, end, i + 1, len(colors)):
            current_time = time.time() * 1000
            print(f"\nNo se pudo conectar el color {color}!")
            print(f"Tiempo transcurrido: {current_time - start_time:.2f} ms")
            return False

    # Exito: todos los colores conectados
    graph.finished = True
    clear_screen()
    current_time = time.time() * 1000
    print("¡SOLUCIÓN ENCONTRADA!")
    print(f"Tiempo total: {current_time - start_time:.2f} ms")
    print(f"Colores conectados: {len(colors)}")
    print_board(graph)
    return True

# Calcula la distancia Manhattan entre dos puntos
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# Conecta dos puntos de un color en el grafo usando A* para encontrar el camino mas corto
def connect_color(graph, color, start, end, current, total):
    open_set = []
    heapq.heappush(open_set, (0, start, [start]))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, end)}

    while open_set:
        _, current_pos, path = heapq.heappop(open_set)

        if current_pos == end:
            # Encontramos un camino, aplicarlo
            apply_path(graph, color, path)
            clear_screen()
            print(f"Conectando color {color} ({current}/{total})...")
            print(f"Longitud del camino: {len(path)} celdas")
            print_board(graph)
            return True

        for neighbor in get_neighbors(graph, current_pos):
            # Verificar si podemos pasar por esta celda
            current_value = graph.matrix[neighbor[0]][neighbor[1]]
            if current_value != 0 and neighbor != end and neighbor != start:
                continue

            # Calcular nuevo costo
            tentative_g_score = g_score[current_pos] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_pos
                g_score[neighbor] = tentative_g_score
                f = tentative_g_score + manhattan_distance(neighbor, end)
                new_path = path + [neighbor]
                heapq.heappush(open_set, (f, neighbor, new_path))

    return False

# Obtiene los vecinos válidos de una celda en el grafo
def get_neighbors(graph, cell):
    i, j = cell
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        ni, nj = i + dx, j + dy
        if 0 <= ni < graph.n and 0 <= nj < graph.m:
            neighbors.append((ni, nj))
    return neighbors

# Aplicar el camino encontrado al grafo
def apply_path(graph, color, path):
    # Aplicar el camino al grafo
    for cell in path[1:-1]:  # No sobrescribir los puntos de inicio/fin
        i, j = cell
        graph.matrix[i][j] = color

    # Actualizar el camino para este color
    graph.paths[color] = path
    graph.connected_paths.add(color)