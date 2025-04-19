#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random

#-------------------------------------------------------------------------
# graph     :   Clase que representa un grafo no dirigido.
# @inputs   :   Parámetros para operaciones sobre el grafo.
# @outputs  :   Resultados de las operaciones sobre el grafo.
# @authors  :   Miguel Marquez & Ivan Dario Orozco Ibanez.
#-------------------------------------------------------------------------
class Graph:
    COLOR_CODES = [31, 32, 33, 34, 35, 36, 91, 92, 93, 94, 95, 96]

    # Constructor de la clase Graph:
    def __init__(self, matrix):
        if not matrix or any(len(r) != len(matrix[0]) for r in matrix):
            raise ValueError("La matriz debe ser no vacía y todas las filas del mismo tamaño")
        self.matrix = [row[:] for row in matrix]
        self.n, self.m = len(matrix), len(matrix[0])
        self._assign_pair_colors()
        self._find_initial_positions()
        # Inicializamos los caminos con solo los endpoints
        self.paths = {v: [p1, p2] for v, (p1, p2) in self.initial_positions.items()}

    # toString:
    def __str__(self):
        return "\n".join(str(row) for row in self.matrix)

    # Asigna un color (foreground y background) único para cada par de números:
    def _assign_pair_colors(self):
        values = sorted({v for row in self.matrix for v in row if v != 0})
        if len(values) > len(self.COLOR_CODES):
            raise ValueError(
                f"Necesito al menos {len(values)} colores únicos, pero solo tengo {len(self.COLOR_CODES)}."
            )
        chosen_fg = random.sample(self.COLOR_CODES, k=len(values))
        self.fg_color_map = {val: chosen_fg[i] for i, val in enumerate(values)}
        # background code = fg + 10 (para ANSI)
        self.bg_color_map = {v: c + 10 for v, c in self.fg_color_map.items()}

    # Localiza los dos endpoints de cada valor en la matriz:
    def _find_initial_positions(self):
        d = {}
        for i in range(self.n):
            for j in range(self.m):
                v = self.matrix[i][j]
                if v != 0:
                    d.setdefault(v, []).append((i, j))
        self.initial_positions = {}
        for v, pts in d.items():
            if len(pts) != 2:
                raise ValueError(f"El valor {v} debe aparecer exactamente dos veces, aparece {len(pts)}.")
            self.initial_positions[v] = (pts[0], pts[1])

    # Definir si la matriz es vacía:
    def is_empty(self):
        return self.n == 0 or self.m == 0

    # Definir las dimensiones de la matriz:
    def dimensions(self):
        return (self.n, self.m)

    # Retornar un valor en la matriz:
    def get_value(self, i, j):
        if not (0 <= i < self.n and 0 <= j < self.m):
            raise IndexError(f"Coordenada ({i},{j}) fuera de rango")
        return self.matrix[i][j]

    # Asignar un valor en la matriz:
    def set_value(self, i, j, v):
        if not (0 <= i < self.n and 0 <= j < self.m):
            raise IndexError(f"Coordenada ({i},{j}) fuera de rango")
        self.matrix[i][j] = v

    # Obtener los vecinos de un nodo (i,j):
    def get_neighbors(self, i, j):
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        vecinos = []
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.n and 0 <= nj < self.m:
                vecinos.append((ni, nj))
        return vecinos

    # Ciclo de juego:
    def start(self):
        # 1. Dibujar o extender camino
        def draw_path():
            try:
                v = int(input("Número a trabajar: "))
                p1, p2 = self.initial_positions[v]
            except:
                print("Número inválido.")
                return
            raw = input("Coords (i,j) separadas por ';' (ej:1,1;1,2;...): ")
            try:
                coords = [tuple(map(int, xy.split(','))) for xy in raw.split(';')]
            except:
                print("Formato inválido.")
                return
            # validar que no se sobreescriban endpoints ni otras rutas
            for coord in coords:
                i, j = coord[0]-1, coord[1]-1
                if coord in [(p1[0]+1,p1[1]+1),(p2[0]+1,p2[1]+1)]:
                    continue
                if not (0 <= i < self.n and 0 <= j < self.m):
                    print(f"{coord} fuera de rango.")
                    return
                if self.matrix[i][j] != 0:
                    print(f"Celda {coord} ocupada.")
                    return
            # limpiar camino previo
            for coord in self.paths[v]:
                if coord not in (p1, p2):
                    i, j = coord
                    self.matrix[i][j] = 0
            # pintar nuevos puntos
            for coord in coords:
                i, j = coord[0]-1, coord[1]-1
                self.matrix[i][j] = v
            # reconstruir lista manteniendo endpoints
            new_path = [p1] + [(c[0]-1,c[1]-1) for c in coords if (c[0]-1,c[1]-1) not in (p1, p2)] + [p2]
            self.paths[v] = new_path
            print("Puntos asignados en el camino.")

        # 2. Borrar camino completo
        def erase_path():
            try:
                v = int(input("Número cuyo camino borrar: "))
                p1, p2 = self.initial_positions[v]
            except:
                print("Número inválido.")
                return
            for coord in self.paths[v]:
                if coord not in (p1, p2):
                    i, j = coord
                    self.matrix[i][j] = 0
            self.paths[v] = [p1, p2]
            print("Camino completo borrado.")

        # 3. Borrar un paso cualquiera
        def erase_step():
            try:
                v = int(input("Número cuyo paso borrar: "))
                path = self.paths[v]
            except:
                print("Número inválido.")
                return
            raw = input("Coord a borrar (i,j): ")
            try:
                coord = tuple(map(int, raw.split(',')))
                coord0 = (coord[0]-1, coord[1]-1)
            except:
                print("Formato inválido.")
                return
            p1, p2 = self.initial_positions[v]
            if coord0 in (p1, p2) or coord0 not in path:
                print("No puedes borrar ese punto.")
                return
            i, j = coord0
            self.matrix[i][j] = 0
            self.paths[v].remove(coord0)
            print("Paso borrado.")

        actions = {
            "1": ("Dibujar/Extender camino", draw_path),
            "2": ("Borrar camino completo", erase_path),
            "3": ("Borrar un paso", erase_step),
            "4": ("Salir", None),
        }
        while True:
            self.print_board()
            print("\nOpciones:")
            for k, (desc, _) in actions.items():
                print(f"{k}. {desc}")
            choice = input("Elige opción: ").strip()
            if choice == "4":
                print("Saliendo.")
                break
            action = actions.get(choice)
            if action:
                action[1]()
            else:
                print("Opción inválida.")

    # Imprimir tablero con índices 1-based, esquina superior izquierda = (1,1)
    def print_board(self):
        # ancho de celda según el valor de mayor longitud
        max_len = max((len(str(v)) for row in self.matrix for v in row if v != 0), default=1)
        w = max_len + 2

        # ancho para la etiqueta de fila
        row_label_w = len(str(self.n))

        # indent para las líneas de borde
        indent = " " * (row_label_w + 1)

        # encabezado de columnas, centrado sobre cada celda
        header = indent + " " + " ".join(str(j+1).center(w) for j in range(self.m))
        print(header)

        # línea horizontal inicial
        print(f"{indent}+" + "+".join("-" * w for _ in range(self.m)) + "+")

        # cada fila: etiqueta i+1 y contenido
        for i, row in enumerate(self.matrix):
            row_label = str(i+1).rjust(row_label_w)
            line = "|"
            for j, v in enumerate(row):
                if v == 0:
                    raw = " " * w
                else:
                    if (i, j) in self.initial_positions[v]:
                        fg = self.fg_color_map[v]
                        txt = str(v).center(w)
                        raw = f"\033[{fg}m{txt}\033[0m"
                    else:
                        bg = self.bg_color_map[v]
                        raw = f"\033[{bg}m{' ' * w}\033[0m"
                line += raw + "|"
            print(f"{row_label} {line}")
            print(f"{indent}+" + "+".join("-" * w for _ in range(self.m)) + "+")