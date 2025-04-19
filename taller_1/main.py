import time
import random
import sys

from taller_1.get_data import get_data
from taller_1.iterative_solution import solucion_iterativa
from taller_1.recursive_solution import solucion_divide_vence

def generar_rectangulos(n):
    """Genera una lista de n rectángulos con coordenadas aleatorias cumpliendo las restricciones del problema."""
    rectangulos = []
    x_prev = 0
    for _ in range(n):
        x_u = x_prev + random.randint(1, 10)
        y_u = random.randint(5, 20)
        x_d = x_u + random.randint(1, 5)
        y_d = y_u - random.randint(1, 5)
        rectangulos.append(((x_u, y_u), (x_d, y_d)))
        x_prev = x_u  # Asegurar x_i^u < x_{i+1}^u
    return rectangulos


def medir_tiempo(S, funcion):
    """Mide el tiempo de ejecución de una función dada con la entrada S."""
    inicio = time.perf_counter_ns()
    funcion(S)
    fin = time.perf_counter_ns()
    return fin - inicio


def ejecutar_experimentos(min_n, max_n, step_n, output_file):
    """Ejecuta los experimentos y guarda los resultados en un archivo de texto."""
    with open(output_file, 'w') as f:
        for n in range(min_n, max_n + step_n, step_n):
            S = generar_rectangulos(n)
            tiempo_iter = medir_tiempo(S, solucion_iterativa)
            tiempo_rec = medir_tiempo(S, solucion_divide_vence)
            f.write(f"{n}, {tiempo_iter}, {tiempo_rec}\n")
            print(f"{n} rectángulos -> Iterativo: {tiempo_iter} ns, Recursivo: {tiempo_rec} ns")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python main.py min_n max_n step_n output_file")
        sys.exit(1)

    min_n = int(sys.argv[1])
    max_n = int(sys.argv[2])
    step_n = int(sys.argv[3])
    output_file = sys.argv[4]

    ejecutar_experimentos(min_n, max_n, step_n, output_file)


