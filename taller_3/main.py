import sys
import time

def calculate_avg_std_iter(numbers):
    """
    Calcula el promedio y la desviación estándar de una lista de números
    El promedio se calcula como la suma de los números dividido por la cantidad de números
    La desviación estándar se calcula como la raíz cuadrada de la suma de la diferencia de cada número
        con el promedio al cuadrado dividido por la cantidad de números
    """
    # TODO: implementar la función, ** sirve en python para elevar a una potencia


def calculate_avg_std_DYV(numbers):
    # Recuerde que en pseudocódigo los indices irian de 1 a |numbers|
    return calculate_avg_std_DYV_aux(numbers, 0, len(numbers)-1)

def calculate_avg_std_DYV_aux(numbers, b, e):
    # TODO: implementar la función
    # Si se tiene una desviacion s1 sobre un conjunto de n1 elementos y una desviacion s2 sobre un conjunto de n2 elementos
    # avg1 el promedio del primer conjunto y avg2 el del segundo, la desviacion sobre el conjunto de n1+n2 elementos es:
    #       (n1*s1^2 + n2*s2^2) / (n1 + n2) + (avg1 - avg2)^2 *(n1*n2)/ (n1 + n2)

    pass


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
