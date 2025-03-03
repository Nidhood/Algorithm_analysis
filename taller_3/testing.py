import unittest
import math, statistics, random
from taller_3.iterative_solution import calculate_avg_std_iter
from taller_3.recursive_solution import calculate_avg_std_DYV

class MyTestCase(unittest.TestCase):
    def test_constant(self):
        constant_sequence= [1]*10
        avg, std = calculate_avg_std_iter(constant_sequence)
        avg_dyv, std_dyv = calculate_avg_std_DYV(constant_sequence)
        self.assertEqual(avg, 1)
        self.assertEqual(std, 0)
        self.assertEqual(avg_dyv, 1)
        self.assertEqual(std_dyv, 0)

    def test_increasing(self):
        increasing_sequence= [i for i in range(10)]
        avg, std = calculate_avg_std_iter(increasing_sequence)
        avg_dyv, std_dyv = calculate_avg_std_DYV(increasing_sequence)
        self.assertEqual(avg, 4.5)
        assert math.isclose(std, math.sqrt(8.25))

        self.assertEqual(avg_dyv, 4.5)
        assert math.isclose(std_dyv, math.sqrt(8.25))

    def test_rand(self):
        place_sequence = [random.randint(1, 20) for i in range(0, 100)]
        avg_ok = statistics.mean(place_sequence)
        std_ok = statistics.stdev(place_sequence)
        avg, std = calculate_avg_std_iter(place_sequence)
        avg_dyv, std_dyv = calculate_avg_std_DYV(place_sequence)
        self.assertEqual(avg, avg_ok)
        assert math.isclose(std, std_ok)

        self.assertEqual(avg_dyv, avg_ok)
        assert math.isclose(std_dyv, std_ok)

if __name__ == '__main__':
    unittest.main()
