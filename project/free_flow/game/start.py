#!/usr/bin/python3
# -*- coding: utf-8 -*-

import collections
from project.free_flow.board.print_board import print_board

#-------------------------------------------------------------------------
# start     :   Funcion que inicia el juego y permite al usuario interactuar
#               con el tablero.
# @inputs   :   Grafo que representa el tablero de juego.
# @outputs  :   Ninguno
# @author   :   Miguel & Ivan Dario Orozco Ibanez
#-------------------------------------------------------------------------

# BFS para verificar si endpoints de valor v están unidos por celdas == v.
def is_connected(graph, v):
    p1, p2 = graph.initial_positions[v]
    dq = collections.deque([p1])
    seen = {p1}
    while dq:
        x, y = dq.popleft()
        if (x, y) == p2:
            return True
        for nx, ny in graph.get_neighbors(x, y):
            if (nx, ny) not in seen and graph.matrix[nx][ny] == v:
                seen.add((nx, ny))
                dq.append((nx, ny))
    return False

# Permite al usuario agregar/trazar pasos en el camino de un valor.
def draw_path(graph):
    if graph.finished:
        print("Ya has ganado: solo puedes salir.")
        return

    try:
        v = int(input("Número a trabajar: ").strip())
        p1, p2 = graph.initial_positions[v]
    except:
        print("Número inválido.")
        return

    raw = input("Coords (i,j) separadas por '-' (ej:1,1-1,2-...): ").strip()
    frags = raw.split('-')
    coords = []
    for frag in frags:
        frag = frag.strip()
        if not frag:
            continue
        parts = frag.split(',')
        if len(parts) != 2:
            print(f"Formato inválido en '{frag}'")
            return
        try:
            i, j = int(parts[0]) - 1, int(parts[1]) - 1
        except:
            print(f"Coordenadas no numéricas en '{frag}'")
            return
        coords.append((i, j))

    # validar y pintar solo nuevas celdas vacías o endpoints
    new_steps = []
    for i, j in coords:
        if not (0 <= i < graph.n and 0 <= j < graph.m):
            print(f"Coord {(i+1,j+1)} fuera de rango.")
            return
        if graph.matrix[i][j] not in (0, v):
            print(f"Celda {(i+1,j+1)} ocupada.")
            return
        if graph.matrix[i][j] == 0:
            graph.matrix[i][j] = v
            new_steps.append((i, j))

    # reconstruir path sin borrar previos
    full = [p1] \
           + [pt for pt in graph.paths[v] if pt not in (p1, p2)] \
           + new_steps + [p2]
    seen = set(); cleaned = []
    for pt in full:
        if pt not in seen:
            cleaned.append(pt)
            seen.add(pt)
    graph.paths[v] = cleaned

    print("Puntos agregados al camino.")

    # detecta conexión
    if v not in graph.connected_paths and is_connected(graph, v):
        graph.connected_paths.add(v)
        print(f"¡Camino {v} se ha conectado!")

    # victoria
    if (len(graph.connected_paths) == len(graph.initial_positions)
        and graph.is_full()):
        graph.finished = True
        print("¡Has ganado! Solo queda salir.")

# Borrar completamente el camino intermedio de un valor, dejando endpoints.
def erase_path(graph):

    if graph.finished:
        print("Ya has ganado: solo puedes salir.")
        return

    try:
        v = int(input("Número cuyo camino borrar: ").strip())
        p1, p2 = graph.initial_positions[v]
    except:
        print("Número inválido.")
        return

    for (i, j) in list(graph.paths[v]):
        if (i, j) not in (p1, p2):
            graph.matrix[i][j] = 0
    graph.paths[v] = [p1, p2]
    graph.connected_paths.discard(v)
    print("Camino completo borrado.")

# Borrar un único paso intermedio de un camino.
def erase_step(graph):

    if graph.finished:
        print("Ya has ganado: solo puedes salir.")
        return

    try:
        v = int(input("Número cuyo paso borrar: ").strip())
    except:
        print("Número inválido.")
        return

    raw = input("Coord a borrar (i,j): ").strip()
    parts = raw.split(',')
    if len(parts) != 2:
        print("Formato inválido.")
        return
    try:
        i, j = int(parts[0]) - 1, int(parts[1]) - 1
    except:
        print("Coordenadas no numéricas.")
        return

    p1, p2 = graph.initial_positions[v]
    if (i, j) in (p1, p2) or (i, j) not in graph.paths[v]:
        print("No puedes borrar ese punto.")
        return

    graph.matrix[i][j] = 0
    graph.paths[v].remove((i, j))
    graph.connected_paths.discard(v)
    print("Paso borrado.")

# Ciclo principal de interacción.
def start(graph):

    actions = {
        "1": ("Dibujar/Extender camino", draw_path),
        "2": ("Borrar camino completo",   erase_path),
        "3": ("Borrar un paso",           erase_step),
        "4": ("Salir",                    None),
    }

    while True:
        print_board(graph)
        print("\nOpciones:")
        for k, (desc, _) in actions.items():
            if graph.finished and k in ("1","2","3"):
                continue
            print(f"{k}. {desc}")

        choice = input("Elige opción: ").strip()
        if choice == "4":
            print("Saliendo.")
            break

        action = actions.get(choice)
        if action and action[1]:
            action[1](graph)
        else:
            print("Opción inválida.")