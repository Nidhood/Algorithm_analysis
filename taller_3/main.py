import sys
import time
from taller_3.iterative_solution import calculate_avg_std_iter
from taller_3.recursive_solution import calculate_avg_std_DYV

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    file = sys.argv[1]
    with open(file, 'r') as f:
        # file should be a one line of numbers separated by space to convert to list
        numbers = list(map(int, f.readline().split()))
        print(numbers)

        # start time useing perf_counter
        start = time.perf_counter()
        avg, std = calculate_avg_std_iter(numbers)
        end = time.perf_counter()
        print(f'tiempo de ejecución: {end - start}')
        print(f'Promedio: {avg} desviación estándar: {std} ')
        start_dyv = time.perf_counter()
        avg_dyv, std_dyv = calculate_avg_std_DYV(numbers)
        end_dyv = time.perf_counter()
        print(f'tiempo de ejecución DYV: {end_dyv - start_dyv}')
        print(f'Promedio dyv: {avg_dyv} desviación estándar: {std_dyv} ')