#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import collections

class Graph:
    COLOR_CODES = [31, 32, 33, 34, 35, 36, 91, 92, 93, 94, 95, 96]

    def __init__(self, matrix):
        if not matrix or any(len(r) != len(matrix[0]) for r in matrix):
            raise ValueError("La matriz debe ser no vacía y todas las filas del mismo tamaño")
        self.matrix = [row[:] for row in matrix]
        self.n, self.m = len(matrix), len(matrix[0])
        self._assign_pair_colors()
        self._find_initial_positions()
        # Inicializamos los caminos con solo los endpoints
        self.paths = {v: [p1, p2] for v, (p1, p2) in self.initial_positions.items()}
        # Seguimiento de caminos conectados y estado de victoria
        self.connected_paths = set()
        self.finished = False

    def __str__(self):
        return "\n".join(str(row) for row in self.matrix)

    def _assign_pair_colors(self):
        values = sorted({v for row in self.matrix for v in row if v != 0})
        if len(values) > len(self.COLOR_CODES):
            raise ValueError(
                f"Necesito al menos {len(values)} colores únicos, "
                f"pero solo tengo {len(self.COLOR_CODES)}."
            )
        chosen_fg = random.sample(self.COLOR_CODES, k=len(values))
        self.fg_color_map = {val: chosen_fg[i] for i, val in enumerate(values)}
        self.bg_color_map = {v: c + 10 for v, c in self.fg_color_map.items()}

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

    def is_empty(self):
        return self.n == 0 or self.m == 0

    def dimensions(self):
        return (self.n, self.m)

    def get_value(self, i, j):
        if not (0 <= i < self.n and 0 <= j < self.m):
            raise IndexError(f"Coordenada ({i},{j}) fuera de rango")
        return self.matrix[i][j]

    def set_value(self, i, j, v):
        if not (0 <= i < self.n and 0 <= j < self.m):
            raise IndexError(f"Coordenada ({i},{j}) fuera de rango")
        self.matrix[i][j] = v

    def get_neighbors(self, i, j):
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        vecinos = []
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.n and 0 <= nj < self.m:
                vecinos.append((ni, nj))
        return vecinos

    def start(self):
        def is_connected(v):
            """Comprueba si p1 y p2 están unidos por un camino de celdas == v."""
            p1, p2 = self.initial_positions[v]
            queue = collections.deque([p1])
            seen = {p1}
            while queue:
                x, y = queue.popleft()
                if (x, y) == p2:
                    return True
                for nx, ny in self.get_neighbors(x, y):
                    if (nx, ny) not in seen and self.matrix[nx][ny] == v:
                        seen.add((nx, ny))
                        queue.append((nx, ny))
            return False

        def draw_path():
            if self.finished:
                print("Ya has ganado, solo puedes salir.")
                return
            try:
                v = int(input("Número a trabajar: "))
                p1, p2 = self.initial_positions[v]
            except:
                print("Número inválido.")
                return
            raw = input("Coords (i,j) separadas por '-' (ej:1,1-1,2-...): ")
            try:
                coords = [tuple(map(int, xy.split(','))) for xy in raw.split('-')]
            except:
                print("Formato inválido.")
                return

            new_steps = []
            for ci, cj in coords:
                i, j = ci-1, cj-1
                if not (0 <= i < self.n and 0 <= j < self.m):
                    print(f"{(ci,cj)} fuera de rango.")
                    return
                if self.matrix[i][j] != 0 and (i,j) not in self.initial_positions[v]:
                    print(f"Celda {(ci,cj)} ocupada.")
                    return
                if self.matrix[i][j] == 0:
                    self.matrix[i][j] = v
                    new_steps.append((i,j))

            p1, p2 = self.initial_positions[v]
            full_path = [p1] + [pt for pt in self.paths[v] if pt not in (p1,p2)] \
                        + new_steps + [p2]
            seen = set(); cleaned = []
            for pt in full_path:
                if pt not in seen:
                    cleaned.append(pt); seen.add(pt)
            self.paths[v] = cleaned

            print("Puntos agregados al camino.")

            if v not in self.connected_paths and is_connected(v):
                self.connected_paths.add(v)
                print(f"¡Camino {v} se ha conectado!")
                if len(self.connected_paths) == len(self.initial_positions):
                    self.finished = True
                    print("¡Has ganado! Sólo puedes salir.")

        def erase_path():
            if self.finished:
                print("Ya has ganado, solo puedes salir.")
                return
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

        def erase_step():
            if self.finished:
                print("Ya has ganado, solo puedes salir.")
                return
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
                if self.finished and k in ("1","2","3"):
                    continue
                print(f"{k}. {desc}")
            choice = input("Elige opción: ").strip()
            if choice == "4":
                print("Saliendo.")
                break
            action = actions.get(choice)
            if action and action[1]:
                action[1]()
            else:
                print("Opción inválida.")

    def print_board(self):
        max_len = max((len(str(v)) for row in self.matrix for v in row if v != 0), default=1)
        w = max_len + 2
        row_label_w = len(str(self.n))
        indent = " " * (row_label_w + 1)

        header = indent + " " + " ".join(str(j+1).center(w) for j in range(self.m))
        print(header)
        print(f"{indent}+" + "+".join("-" * w for _ in range(self.m)) + "+")

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