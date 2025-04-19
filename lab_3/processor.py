import sys
import os
import math
from tabulate import tabulate


# Definimos las funciones de test.py directamente aquí para evitar problemas de importación
def ActivitySelector_GREEDY(C):
    A = sorted(C, key=lambda c: c[2])
    R = [A[0]]
    k = 0
    for m in range(1, len(A)):
        if A[m][1] >= A[k][2]:
            R += [A[m]]
            k = m
    return R


def ActivitySelector_DP_Aux(A, i, j, M):
    if M[i][j] == -math.inf:
        S = []
        for k in range(i, j + 1):
            if A[k][1] >= A[i][2] and A[k][2] <= A[j][1]:
                S.append(k)

        if len(S) == 0:
            M[i][j] = 0
        else:
            q = -math.inf
            for k in S:
                v = 1 + ActivitySelector_DP_Aux(A, i, k, M)
                v = v + ActivitySelector_DP_Aux(A, k, j, M)
                if q < v:
                    q = v
            M[i][j] = q
    return M[i][j]


def ActivitySelector_DP(A):
    C = sorted(A, key=lambda a: a[2])
    C.insert(0, ["__not_valid__", -math.inf, 0])
    C.append(["__not_valid__", C[-1][2], math.inf])
    M = [[-math.inf for j in range(len(C))] for i in range(len(C))]
    return ActivitySelector_DP_Aux(C, 0, len(C) - 1, M)


# Función para obtener el rango de slots de un archivo de actividades
def get_slot_range(file_path):
    min_slot = float('inf')
    max_slot = float('-inf')

    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                start = int(parts[1])
                end = int(parts[2])
                min_slot = min(min_slot, start)
                max_slot = max(max_slot, end)

    return min_slot, max_slot


# Función para contar el número de actividades en un archivo
def count_activities(file_path):
    count = 0
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                count += 1
    return count


# Función para leer datos del archivo
def read_data_from_file(file_path):
    data = []
    with open(file_path) as f:
        for line in f:
            for t in line.split('\n'):
                d = t.split(' ')
                if len(d) >= 3:
                    data.append([d[0], int(d[1]), int(d[2])])
    return data


# Función para procesar un archivo
def process_file(file_path):
    # Leer datos del archivo
    data = read_data_from_file(file_path)

    # Calcular resultados de greedy y programación dinámica
    greedy_result = len(ActivitySelector_GREEDY(data))
    dp_result = ActivitySelector_DP(data)

    return greedy_result, dp_result


def main():
    if len(sys.argv) < 2:
        print("Uso: python3", sys.argv[0], "archivo1 archivo2 ... archivoN")
        print("   o: python3", sys.argv[0], "número_de_archivos")
        sys.exit(1)

    # Determinar qué archivos procesar
    files_to_process = []

    # Si solo hay un argumento y es un número, procesar tantos archivos sequenciales
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        num_files = int(sys.argv[1])
        files_to_process = [f"activities_{i}" for i in range(1, num_files + 1)]
    else:
        # Si se especifican nombres de archivos explícitamente
        files_to_process = sys.argv[1:]

    # Verificar que los archivos existen
    valid_files = []
    for file in files_to_process:
        if not os.path.exists(file):
            print(f"Advertencia: El archivo '{file}' no existe y será omitido.")
        else:
            valid_files.append(file)

    if not valid_files:
        print("Error: Ninguno de los archivos especificados existe.")
        sys.exit(1)

    # Procesar cada archivo y almacenar resultados
    results = []
    total_files = len(valid_files)

    for i, file in enumerate(valid_files):
        try:
            print(f"Procesando archivo {i + 1}/{total_files}: {file}")

            # Obtener número de actividades
            num_activities = count_activities(file)

            # Obtener rango de slots
            min_slot, max_slot = get_slot_range(file)
            slot_range = f"{min_slot}-{max_slot}"

            # Ejecutar algoritmos y obtener resultados
            greedy_result, dp_result = process_file(file)

            # Almacenar resultados
            results.append([file, num_activities, slot_range, greedy_result, dp_result])

        except Exception as e:
            print(f"Error al procesar '{file}': {str(e)}")
            results.append([file, "ERROR", "ERROR", "ERROR", "ERROR"])

    # Mostrar resultados en una tabla
    headers = ["Archivo", "Actividades", "Rango de slots", "Greedy", "Prog. Dinámica"]
    print(tabulate(results, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()