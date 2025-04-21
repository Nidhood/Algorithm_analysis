#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import collections

class Graph:
    COLOR_CODES = [31, 32, 33, 34, 35, 36,
                   91, 92, 93, 94, 95, 96]

    def __init__(self, matrix):
        if not matrix or any(len(r) != len(matrix[0]) for r in matrix):
            raise ValueError(
                "La matriz debe ser no vacía y todas las filas del mismo tamaño"
            )
        # copiar matriz
        self.matrix = [row[:] for row in matrix]
        self.n, self.m = len(matrix), len(matrix[0])

        # asignar colores a cada par de endpoints
        self._assign_pair_colors()
        # localizar posiciones iniciales de cada valor
        self._find_initial_positions()

        # almacena lista de coordenadas de cada camino (empieza solo con endpoints)
        self.paths = {
            v: [p1, p2]
            for v, (p1, p2) in self.initial_positions.items()
        }

        # seguimiento de caminos ya conectados y bandera de terminado
        self.connected_paths = set()
        self.finished = False

    def _assign_pair_colors(self):
        values = sorted({
            v for row in self.matrix for v in row if v != 0
        })
        if len(values) > len(self.COLOR_CODES):
            raise ValueError(
                f"Necesito al menos {len(values)} colores, pero solo hay "
                f"{len(self.COLOR_CODES)} disponibles."
            )
        chosen = random.sample(self.COLOR_CODES, k=len(values))
        self.fg_color_map = {v: chosen[i] for i, v in enumerate(values)}
        # color de fondo = fg + 10
        self.bg_color_map = {v: fg + 10 for v, fg in self.fg_color_map.items()}

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
                raise ValueError(
                    f"El valor {v} debe aparecer exactamente dos veces, "
                    f"aparece {len(pts)}."
                )
            self.initial_positions[v] = (pts[0], pts[1])

    def get_neighbors(self, i, j):
        """Vecinos 4‑direccionales dentro de límites."""
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.n and 0 <= nj < self.m:
                yield (ni, nj)

    def is_full(self):
        """¿No queda ni un solo 0 en la matriz?"""
        return all(
            self.matrix[i][j] != 0
            for i in range(self.n) for j in range(self.m)
        )