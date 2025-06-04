import sys
import numpy as np
import time


def mat_mult_aux(d, i, j):
    if i == j:
        return 0
    else:
        cost = float('inf')
        for k in range(i, j):
            op = mat_mult_aux(d,i,k)+mat_mult_aux(d, k+1, j) + d[i-1]*d[k]*d[j]
            if op < cost:
                cost = op
        return cost

def mat_mult(A):
    init = time.perf_counter_ns()
    n = len(A)
    cost = mat_mult_aux(A, 1, n - 1)

    end = time.time_ns()
    print(f' Total time is: {(end - init)}')
    return cost

def mat_mult_memo(d, i, j, memo):
    if i == j:
        return 0
    if memo[i][j] is not None:
        return memo[i][j]
    cost = float('inf')
    for k in range(i, j):
        op = (mat_mult_memo(d, i, k, memo) +
              mat_mult_memo(d, k + 1, j, memo) +
              d[i - 1] * d[k] * d[j])
        if op < cost:
            cost = op
    memo[i][j] = cost
    return cost

def mat_mult_dp(d):
    n = len(d)
    memo = [[None] * n for _ in range(n)]
    return mat_mult_memo(d, 1, n - 1, memo)


def mat_mult_bottom_up(d):
    n = len(d)
    # Inicializar la tabla con 0 para el caso base
    m = [[0 for _ in range(n)] for _ in range(n)]

    # l es la longitud de la cadena (a partir de 2 matrices)
    for l in range(2, n):
        for i in range(1, n - l + 1):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + d[i - 1] * d[k] * d[j]
                if q < m[i][j]:
                    m[i][j] = q
    return m[1][n - 1]


# end def

## -------------------------------------------------------------------------
if len(sys.argv) < 2:
    print("Usage: python3", sys.argv[0], "input_file")
    sys.exit(1)
# end if

Af = open(sys.argv[1], 'r').readlines()
A = [int(a) for a in Af][0:]

# Ahora vamos a crear la funcion de memoria, para reducir la complejidad de la funcion.

print(A)
print(mat_mult(A))
print(mat_mult_dp(A))
print(mat_mult_bottom_up(A))