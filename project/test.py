# File: test.py
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import builtins
from free_flow.board.read_board import read_board
from free_flow.graph.graph import Graph
from free_flow.game.start import draw_path
from autonomous_solutions.heuristic_solution import heuristic_solution
from autonomous_solutions.brute_solution import brute_solution

class TestFreeFlow(unittest.TestCase):

    def setUp(self):
        self.board_path = "inputs/board_5.txt"
        self.graph = Graph(read_board(self.board_path))
        self.board_5_path = "inputs/board_5.txt"
        self.board_1_path = "inputs/board_1.txt"
        self.graph_5 = Graph(read_board(self.board_5_path))
        self.graph_1 = Graph(read_board(self.board_1_path))

    def test_orthogonal_moves_only(self):
        import builtins
        graph = Graph(read_board(self.board_5_path))

        # Forzar inicio desde solo un endpoint
        graph.paths[1] = [graph.initial_positions[1][0]]

        # Movimiento en diagonal: NO permitido
        input_values = ["1", "1,2-2,3"]

        def mock_input(_=None):
            return input_values.pop(0)

        original_input = builtins.input
        builtins.input = mock_input
        try:
            t_msgs, _ = draw_path(graph)
        finally:
            builtins.input = original_input

        for msg in t_msgs:
            print("Mensaje recibido:", msg)

        self.assertTrue(
            any("movimiento invalido" in msg.lower() or "movimiento inválido" in msg.lower() for msg in t_msgs),
            "No se detectó el mensaje de movimiento inválido"
        )

    def test_path_from_any_endpoint(self):
        g = Graph(read_board(self.board_5_path))

        # Forzamos el orden inverso de los endpoints
        g.paths[1] = [g.initial_positions[1][1], g.initial_positions[1][0]]

        input_values = ["1", "1,6-1,5"]  # Movimiento desde el segundo endpoint (1,7) → (1,6) → (1,5)

        def mock_input(_=None): return input_values.pop(0)

        original_input = builtins.input
        builtins.input = mock_input
        try:
            t_msgs, _ = draw_path(g)
        finally:
            builtins.input = original_input

        self.assertTrue(
            any("puntos agregados" in msg.lower() for msg in t_msgs),
            "No se detectó confirmación de puntos agregados al empezar desde cualquier endpoint."
        )

    def test_manual_game_win(self):
        g = Graph(read_board(self.board_5_path))
        for v, (p1, p2) in g.initial_positions.items():
            path = [p1]
            i1, j1 = p1
            i2, j2 = p2
            while i1 != i2:
                i1 += 1 if i1 < i2 else -1
                path.append((i1, j1))
            while j1 != j2:
                j1 += 1 if j1 < j2 else -1
                path.append((i1, j1))
            path.append(p2)
            for (i, j) in path[1:-1]:
                g.matrix[i][j] = v
            g.paths[v] = path
            g.connected_paths.add(v)
        g.finished = g.is_full() and len(g.connected_paths) == len(g.initial_positions)
        self.assertTrue(g.finished)

    def test_heuristic_solution_success(self):
        g = Graph(read_board(self.board_5_path))
        result = heuristic_solution(g)
        self.assertTrue(result)
        self.assertTrue(g.finished)

    def test_brute_solution_success(self):
        g = Graph(read_board(self.board_5_path))
        result = brute_solution(g)
        self.assertTrue(result)
        self.assertTrue(g.finished)

    def test_unsolvable_board(self):
        g1 = Graph(read_board(self.board_1_path))
        h_result = heuristic_solution(g1)
        b_result = brute_solution(g1)
        self.assertFalse(h_result)
        self.assertFalse(b_result)


if __name__ == "__main__":
    unittest.main()
