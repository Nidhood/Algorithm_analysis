#!/usr/bin/python3
# -*- coding: utf-8 -*-

import collections
from free_flow.board.print_board import print_board
from utils.clear_screen import clear_screen


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
    transient = []
    persistent = []

    if graph.finished:
        transient.append("Ya has ganado: solo puedes salir.")
        return transient, persistent

    try:
        v = int(input("Número a trabajar: ").strip())
        p1, p2 = graph.initial_positions[v]
    except:
        transient.append("Número inválido.")
        return transient, persistent

    raw = input("Coords (i,j) separadas por '-' (ej:1,1-1,2-...): ").strip()
    frags = raw.split('-')
    coords = []
    for frag in frags:
        frag = frag.strip()
        if not frag:
            continue
        parts = frag.split(',')
        if len(parts) != 2:
            transient.append(f"Formato inválido en '{frag}'")
            return transient, persistent
        try:
            i, j = int(parts[0]) - 1, int(parts[1]) - 1
        except:
            transient.append(f"Coordenadas no numéricas en '{frag}'")
            return transient, persistent
        coords.append((i, j))

    existing = graph.paths[v]

    # Si no hay pasos intermedios, determinar desde qué endpoint empezar
    if len(existing) == 2:
        first_coord = coords[0]
        adj_to_p1 = abs(first_coord[0] - p1[0]) + abs(first_coord[1] - p1[1]) == 1
        adj_to_p2 = abs(first_coord[0] - p2[0]) + abs(first_coord[1] - p2[1]) == 1

        if adj_to_p1:
            existing = [p1, p2]
        elif adj_to_p2:
            existing = [p2, p1]  # invertir endpoints
        else:
            transient.append("Debe empezar desde uno de los endpoints.")
            return transient, persistent

        graph.paths[v] = existing

    if len(graph.paths[v]) > 2:
        prev = graph.paths[v][-2]
    else:
        prev = graph.paths[v][0]

    new_steps = []
    # Validar y pintar nuevas celdas con chequeo de adyacencia
    for (i, j) in coords:
        if not (0 <= i < graph.n and 0 <= j < graph.m):
            transient.append(f"Coord {(i+1, j+1)} fuera de rango.")
            return transient, persistent
        if graph.matrix[i][j] not in (0, v):
            transient.append(f"Celda {(i+1, j+1)} ocupada.")
            return transient, persistent
        if abs(i - prev[0]) + abs(j - prev[1]) != 1:
            transient.append("Movimiento inválido: los movimientos deben ser ortogonales y consecutivos.")
            return transient, persistent
        if graph.matrix[i][j] == 0:
            graph.matrix[i][j] = v
            new_steps.append((i, j))
        prev = (i, j)

    # Reconstruir lista completa de camino:
    start_pt = graph.paths[v][0]
    end_pt = graph.paths[v][-1]
    internal = [pt for pt in graph.paths[v] if pt not in (start_pt, end_pt)]
    full = [start_pt] + internal + new_steps + [end_pt]
    seen_pts = set()
    cleaned = []
    for pt in full:
        if pt not in seen_pts:
            cleaned.append(pt)
            seen_pts.add(pt)
    graph.paths[v] = cleaned

    transient.append("Puntos agregados al camino.")

    if v not in graph.connected_paths and is_connected(graph, v):
        graph.connected_paths.add(v)
        persistent.append(f"¡Camino {v} se ha conectado!")

    # Victoria
    if (len(graph.connected_paths) == len(graph.initial_positions)
            and graph.is_full()):
        graph.finished = True
        transient.append("¡Has ganado! Solo queda salir.")

    return transient, persistent

# Borrar completamente el camino intermedio de un valor, dejando endpoints.
def erase_path(graph):
    transient = []
    persistent = []

    if graph.finished:
        transient.append("Ya has ganado: solo puedes salir.")
        return transient, persistent

    try:
        v = int(input("Número cuyo camino borrar: ").strip())
        p1, p2 = graph.initial_positions[v]
    except:
        transient.append("Número inválido.")
        return transient, persistent

    for (i, j) in list(graph.paths[v]):
        if (i, j) not in (p1, p2):
            graph.matrix[i][j] = 0
    graph.paths[v] = [p1, p2]
    graph.connected_paths.discard(v)
    transient.append("Camino completo borrado.")
    return transient, persistent

# Borrar un único paso intermedio de un camino.
def erase_step(graph):
    transient = []
    persistent = []

    if graph.finished:
        transient.append("Ya has ganado: solo puedes salir.")
        return transient, persistent

    try:
        v = int(input("Número cuyo paso borrar: ").strip())
    except:
        transient.append("Número inválido.")
        return transient, persistent

    raw = input("Coord a borrar (i,j): ").strip()
    parts = raw.split(',')
    if len(parts) != 2:
        transient.append("Formato inválido.")
        return transient, persistent
    try:
        i, j = int(parts[0]) - 1, int(parts[1]) - 1
    except:
        transient.append("Coordenadas no numéricas.")
        return transient, persistent

    p1, p2 = graph.initial_positions[v]
    if (i, j) in (p1, p2) or (i, j) not in graph.paths[v]:
        transient.append("No puedes borrar ese punto.")
        return transient, persistent

    graph.matrix[i][j] = 0
    graph.paths[v].remove((i, j))
    graph.connected_paths.discard(v)
    transient.append("Paso borrado.")
    return transient, persistent

# Ciclo principal de interacción.
def start(graph):
    persistent_messages = []
    transient_messages = []

    actions = {
        "1": ("Dibujar/Extender camino", draw_path),
        "2": ("Borrar camino completo",   erase_path),
        "3": ("Borrar un paso",           erase_step),
        "4": ("Salir",                    None),
    }

    while True:
        clear_screen()

        # Mostrar mensajes persistentes (conexiones previas)
        for msg in persistent_messages:
            print(msg)

        # Mostrar mensajes transitorios (solo de la última acción)
        for msg in transient_messages:
            print(msg)

        # Limpiar solo los transitorios para la siguiente iteracion
        transient_messages.clear()

        print_board(graph)
        print("\nOpciones:")
        for k, (desc, _) in actions.items():
            if graph.finished and k in ("1", "2", "3"):
                continue
            print(f"{k}. {desc}")

        choice = input("Elige opcion: ").strip()
        if choice == "4":
            transient_messages.append("Saliendo.")
            return graph.finished

        action = actions.get(choice)
        if action and action[1]:
            t_msgs, p_msgs = action[1](graph)
            transient_messages.extend(t_msgs)
            persistent_messages.extend(p_msgs)
        else:
            transient_messages.append("Opcion invalida.")