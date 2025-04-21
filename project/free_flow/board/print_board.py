#!/usr/bin/python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------
# print_board :  Imprime el tablero de juego en la consola.
# @inputs   :   Grafo que representa el tablero de juego.
# @outputs  :   Ninguno
# @author   :   Miguel & Ivan Dario Orozco Ibanez
#-------------------------------------------------------------------------

def print_board(graph):
    # ancho de celda según longitud máxima de cualquier etiqueta
    max_len = max(
        (len(str(v)) for row in graph.matrix for v in row if v != 0),
        default=1
    )
    w = max_len + 2
    row_label_w = len(str(graph.n))
    indent = " " * (row_label_w + 1)

    # encabezado de columnas
    header = indent + " " + " ".join(str(j+1).center(w) for j in range(graph.m))
    print(header)
    # línea superior
    print(f"{indent}+" + "+".join("-" * w for _ in range(graph.m)) + "+")

    for i, row in enumerate(graph.matrix):
        row_label = str(i+1).rjust(row_label_w)
        line = "|"
        for j, v in enumerate(row):
            if v == 0:
                cell = " " * w
            else:
                if (i, j) in graph.initial_positions[v]:
                    # dibujar valor con color de primer plano
                    fg = graph.fg_color_map[v]
                    txt = str(v).center(w)
                    cell = f"\033[{fg}m{txt}\033[0m"
                else:
                    # pintar fondo
                    bg = graph.bg_color_map[v]
                    cell = f"\033[{bg}m{' ' * w}\033[0m"
            line += cell + "|"
        print(f"{row_label} {line}")
        print(f"{indent}+" + "+".join("-" * w for _ in range(graph.m)) + "+")