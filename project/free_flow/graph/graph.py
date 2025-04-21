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
        # Inicializa los caminos con solo los endpoints
        self.paths = {v: [p1, p2] for v, (p1, p2) in self.initial_positions.items()}
        self.connected_paths = set()
        self.finished = False

    def _assign_pair_colors(self):
        values = sorted({v for row in self.matrix for v in row if v != 0})
        if len(values) > len(self.COLOR_CODES):
            raise ValueError(f"Necesito al menos {len(values)} colores únicos, "
                             f"pero solo tengo {len(self.COLOR_CODES)}.")
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

    def get_neighbors(self, i, j):
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        vecinos = []
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.n and 0 <= nj < self.m:
                vecinos.append((ni, nj))
        return vecinos

    def is_full(self):
        return all(self.matrix[i][j] != 0 for i in range(self.n) for j in range(self.m))

    def start(self):
        """Ciclo de juego principal."""
        def is_connected(v):
            """Comprueba si p1 y p2 están unidos por un camino de celdas == v."""
            p1, p2 = self.initial_positions[v]
            q = collections.deque([p1])
            seen = {p1}
            while q:
                x, y = q.popleft()
                if (x, y) == p2:
                    return True
                for nx, ny in self.get_neighbors(x, y):
                    if (nx, ny) not in seen and self.matrix[nx][ny] == v:
                        seen.add((nx, ny))
                        q.append((nx, ny))
            return False

        def draw_path():
            if self.finished:
                print("Ya has ganado: sólo puedes salir.")
                return
            try:
                v = int(input("Número a trabajar: ").strip())
                p1, p2 = self.initial_positions[v]
            except:
                print("Número inválido.")
                return

            raw = input("Coords (i,j) separadas por '-' (ej:1,1-1,2-...): ").strip()
            parts = raw.split('-')
            coords = []
            for frag in parts:
                frag = frag.strip()
                if not frag:
                    continue
                sub = frag.split(',')
                if len(sub) != 2:
                    print(f"Formato inválido en '{frag}': debe ser i,j")
                    return
                try:
                    ci, cj = int(sub[0]), int(sub[1])
                except:
                    print(f"Coordenadas no numéricas en '{frag}'.")
                    return
                coords.append((ci-1, cj-1))

            # Validar y pintar sólo en celdas vacías o endpoints
            new_steps = []
            for i, j in coords:
                if not (0 <= i < self.n and 0 <= j < self.m):
                    print(f"Coordenada {(i+1,j+1)} fuera de rango.")
                    return
                if self.matrix[i][j] != 0 and (i,j) not in (p1, p2):
                    print(f"Celda {(i+1,j+1)} ya ocupada.")
                    return
                if self.matrix[i][j] == 0:
                    self.matrix[i][j] = v
                    new_steps.append((i, j))

            # Actualizar self.paths[v] sin borrar pasos previos
            full = [p1] + [pt for pt in self.paths[v] if pt not in (p1,p2)] \
                   + new_steps + [p2]
            seen = set(); cleaned = []
            for pt in full:
                if pt not in seen:
                    cleaned.append(pt); seen.add(pt)
            self.paths[v] = cleaned

            print("Puntos agregados al camino.")

            # Detectar conexión
            if v not in self.connected_paths and is_connected(v):
                self.connected_paths.add(v)
                print(f"¡Camino {v} se ha conectado!")

            # Condición de victoria: todos conectados y tablero lleno
            if len(self.connected_paths) == len(self.initial_positions) and self.is_full():
                self.finished = True
                print("¡Has ganado! Sólo queda salir.")

        def erase_path():
            if self.finished:
                print("Ya has ganado: sólo puedes salir.")
                return
            try:
                v = int(input("Número cuyo camino borrar: ").strip())
                p1, p2 = self.initial_positions[v]
            except:
                print("Número inválido.")
                return
            for coord in list(self.paths[v]):
                if coord not in (p1, p2):
                    i, j = coord
                    self.matrix[i][j] = 0
            self.paths[v] = [p1, p2]
            self.connected_paths.discard(v)
            print("Camino completo borrado.")

        def erase_step():
            if self.finished:
                print("Ya has ganado: sólo puedes salir.")
                return
            try:
                v = int(input("Número cuyo paso borrar: ").strip())
                path = self.paths[v]
            except:
                print("Número inválido.")
                return
            raw = input("Coord a borrar (i,j): ").strip()
            sub = raw.split(',')
            if len(sub) != 2:
                print("Formato inválido: debe ser i,j")
                return
            try:
                i, j = int(sub[0]) - 1, int(sub[1]) - 1
            except:
                print("Coordenadas no numéricas.")
                return
            p1, p2 = self.initial_positions[v]
            if (i, j) in (p1, p2) or (i, j) not in path:
                print("No puedes borrar ese punto.")
                return
            self.matrix[i][j] = 0
            self.paths[v].remove((i, j))
            self.connected_paths.discard(v)
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
                        raw = f"\033[{fg}m{str(v).center(w)}\033[0m"
                    else:
                        bg = self.bg_color_map[v]
                        raw = f"\033[{bg}m{' ' * w}\033[0m"
                line += raw + "|"
            print(f"{row_label} {line}")
            print(f"{indent}+" + "+".join("-" * w for _ in range(self.m)) + "+")
