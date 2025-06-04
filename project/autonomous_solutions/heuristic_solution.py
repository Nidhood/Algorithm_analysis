# File: autonomous_solutions/heuristic_solution.py
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import math
import random
import itertools
from copy import deepcopy
from free_flow.graph.graph import Graph
from free_flow.board.print_board import print_board
from utils.clear_screen import clear_screen

#-------------------------------------------------------------------------
# dfs_path:   Busca recursivamente un camino desde 'cur' hasta el endpoint p2
#             en 'g_local', marcando celdas libres o el endpoint. Si llega a p2,
#             registra el camino en g_local.paths[color], añade color a
#             g_local.connected_paths y pinta el camino en g_local.matrix.
#             Imprime el tablero con print_board tras completar el camino.
# @inputs   :   color: valor entero del color que conecta.
#               path: lista de tuplas (i,j) representando el camino actual.
#               g_local: instancia de Graph parcial.
# @outputs  :   True si logra conectar hasta p2; False en otro caso.
#-------------------------------------------------------------------------

def dfs_path(color, path, g_local):
    cur = path[-1]
    p2 = g_local.initial_positions[color][1]
    if cur == p2:
        # Ruta completa para este color
        g_local.paths[color] = deepcopy(path)
        g_local.connected_paths.add(color)
        for (i, j) in path:
            g_local.matrix[i][j] = color
        # Imprimir avance
        clear_screen()
        print(f"Conectando color {color}:")
        print_board(g_local)
        time.sleep(0.3)
        return True

    x, y = cur
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < g_local.n and 0 <= ny < g_local.m:
            if (nx, ny) not in path and (g_local.matrix[nx][ny] == 0 or (nx, ny) == p2):
                path.append((nx, ny))
                prev = g_local.matrix[nx][ny]
                g_local.matrix[nx][ny] = color
                if dfs_path(color, path, g_local):
                    return True
                g_local.matrix[nx][ny] = prev
                path.pop()
    return False

#-------------------------------------------------------------------------
# try_order:   Dados 'graph' original y una permutación 'order' de colores,
#              crea una copia profunda, marca endpoints en matrix, y para cada
#              color en 'order' invoca dfs_path. Si todos se conectan, retorna
#              la copia modificada; si falla algún color, retorna None.
# @inputs   :   graph: instancia de Graph original.
#               order: tupla de valores (colores) en el orden a conectar.
# @outputs  :   Graph copia con rutas conectadas o None.
#-------------------------------------------------------------------------

def try_order(graph, order):
    gcopy = deepcopy(graph)
    gcopy.paths = {v: [gcopy.initial_positions[v][0], gcopy.initial_positions[v][1]] for v in order}
    gcopy.connected_paths.clear()
    # Asegurar endpoints marcados en matrix
    for v in order:
        p1, p2 = gcopy.initial_positions[v]
        gcopy.matrix[p1[0]][p1[1]] = v
        gcopy.matrix[p2[0]][p2[1]] = v

    # Conectar colores en el orden dado
    for color in order:
        p1, _ = gcopy.initial_positions[color]
        path = [p1]
        gcopy.matrix[p1[0]][p1[1]] = color
        if not dfs_path(color, path, gcopy):
            return None  # falla este orden
    return gcopy  # éxito: todos conectados

#-------------------------------------------------------------------------
# heuristic_solution:   Intenta conectar todos los pares usando un backtracking
#                      y probando varias permutaciones de orden de colores.
#                      Imprime el tablero tras cada conexión de color, y al
#                      final muestra el número de iteraciones y el tiempo.
# @inputs   :   graph: instancia de Graph inicializada con matrix e initial_positions.
# @outputs  :   True si encuentra solución para al menos un orden; False en otro caso.
#-------------------------------------------------------------------------

def heuristic_solution(graph: Graph):
    sys.setrecursionlimit(10000)
    colores = list(graph.initial_positions.keys())
    k = len(colores)

    # Calcular cuántos órdenes probar:
    # Si k! <= 720, probar todas las permutaciones; si k! > 720, probar 720 órdenes aleatorios.
    total_perm = math.factorial(k)
    if total_perm <= 720:
        orders = list(itertools.permutations(colores))
    else:
        orders = set()
        while len(orders) < 720:
            perm = tuple(random.sample(colores, k))
            orders.add(perm)
        orders = list(orders)

    start_time = time.time()
    iter_count = 0

    # Probar cada orden hasta encontrar solución
    for order in orders:
        iter_count += 1
        result = try_order(graph, order)
        if result is not None:
            # Copiar resultado al graph original
            graph.matrix = result.matrix
            graph.paths = result.paths
            graph.connected_paths = result.connected_paths
            graph.finished = True
            clear_screen()
            elapsed = time.time() - start_time
            print(f"Solución encontrada con orden: {order}")
            print_board(graph)
            print(f"Iteraciones: {iter_count}")
            print(f"Tiempo: {elapsed:.2f} segundos")
            return True

    elapsed = time.time() - start_time
    print(f"Ninguna permutación encontró solución en {iter_count} iteraciones y {elapsed:.2f} segundos.")
    return False
