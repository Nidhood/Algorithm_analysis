#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
from taller_3.solucion_dinamica import top_down, bottom_up, memory_analysis

class TestConstantDifferenceSequence(unittest.TestCase):
    def assert_sequence(self, P, expected_len, expected_seq):
        # Top‑Down
        best_td, M_td = top_down(P)
        self.assertEqual(best_td, expected_len, f"Top‑Down length for {P}")
        seq_td = memory_analysis(P, M_td)
        self.assertEqual(seq_td, expected_seq, f"Top‑Down sequence for {P}")

        # Bottom‑Up
        best_bu, M_bu = bottom_up(P)
        self.assertEqual(best_bu, expected_len, f"Bottom‑Up length for {P}")
        seq_bu = memory_analysis(P, M_bu)
        self.assertEqual(seq_bu, expected_seq, f"Bottom‑Up sequence for {P}")

    def test_empty(self):
        P = []
        self.assert_sequence(P, 0, [])

    def test_single(self):
        P = [7]
        self.assert_sequence(P, 1, [7])

    def test_constant(self):
        P = [5, 5, 5, 5]
        # no diff ≠ 0, so only individual elements
        self.assert_sequence(P, 1, [5])

    def test_strict_increasing(self):
        P = [1, 2, 3, 4, 5]
        self.assert_sequence(P, 5, [1, 2, 3, 4, 5])

    def test_strict_decreasing(self):
        P = [5, 4, 3, 2, 1]
        self.assert_sequence(P, 5, [5, 4, 3, 2, 1])

    def test_example(self):
        P = [15, 14, 16, 18, 17, 5]
        # longest run is [14,16,18]
        self.assert_sequence(P, 3, [14, 16, 18])

    def test_varying_differences(self):
        P = [1, 2, 3, 5, 7, 9]
        # two runs: diff=1 gives [1,2,3] len=3; diff=2 gives [3,5,7,9] len=4
        self.assert_sequence(P, 4, [3, 5, 7, 9])

    def test_alternating(self):
        P = [1, 3, 1, 3, 1, 3]
        # all runs have length 2 ([1,3] or [3,1])
        # first occurs at start
        self.assert_sequence(P, 2, [1, 3])

    def test_end_run(self):
        P = [10, 8, 6, 4, 2, 3]
        # diff=-2 run [10,8,6,4,2] len=5; then breaks
        self.assert_sequence(P, 5, [10, 8, 6, 4, 2])

if __name__ == '__main__':
    unittest.main()
