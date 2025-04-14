import sys
import time

# -------------------------------------------------------------
# Estrategia 1: Algoritmo recusivo ingenuo (Innocent Recursion)
# -------------------------------------------------------------
def mat_mult_aux(d, i, j):
    if i == j:
        return 0
    else:
        cost = float('inf')
        for k in range(i, j):
            op = (mat_mult_aux(d, i, k) +
                  mat_mult_aux(d, k+1, j) +
                  d[i-1] * d[k] * d[j])
            if op < cost:
                cost = op
        return cost

def mat_mult(A):
    init = time.perf_counter_ns()
    n = len(A)
    cost = mat_mult_aux(A, 1, n - 1)
    end = time.perf_counter_ns()
    print(f'Total time is (IR): {end - init} ns')
    return cost

# -------------------------------------------------------------
# Estrategia 2: Top‑Down con memoización (Dynamic Programming)
# -------------------------------------------------------------
def mat_mult_dp(d):
    n = len(d)
    # Creamos la matriz de memoización de tamaño n x n
    memo = [[None] * n for _ in range(n)]
    init = time.perf_counter_ns()
    cost = mat_mult_memo(d, 1, n - 1, memo)
    end = time.perf_counter_ns()
    print(f'Total time is (DP): {end - init} ns')
    return cost

def mat_mult_memo(d, i, j, memo):
    if i == j:
        return 0
    if memo[i][j] is not None:
        return memo[i][j]
    cost = float('inf')
    for k in range(i, j):
        op = (mat_mult_memo(d, i, k, memo) +
              mat_mult_memo(d, k+1, j, memo) +
              d[i-1] * d[k] * d[j])
        if op < cost:
            cost = op
    memo[i][j] = cost
    return cost

# -------------------------------------------------------------
# Código de prueba (main)
# -------------------------------------------------------------
if len(sys.argv) < 2:
    print("Usage: python3", sys.argv[0], "input_file")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    Af = f.readlines()

# Se asume que el archivo contiene números (dimensiones) separados por espacios o líneas.
A = [int(a) for a in Af][0:]

print("Input dimensions:", A)
print("Innocent recursive algorithm cost:", mat_mult(A))
print("Memoized cost:", mat_mult_dp(A))
