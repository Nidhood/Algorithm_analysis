import math

def MVE(S, C):
    S = [0] + S + [0]
    return MVE_rec(S,0, 1, C)

def MVE_rec(S, i, j, c):
    if j >= len(S) or c == 0:
        return 0
    if S[j] > c:
        return MVE_rec(S, i, j + 1, c)
    descartar = MVE_rec(S, i, j + 1, c)
    incluir = S[j] + MVE_rec(S, j, j + 1, c - S[j])

    return max(descartar, incluir)

def MVM(S,C):
    S = [0] + S + [0]
    n = len(S)
    M = [[-math.inf] * (n) for _ in range(1, n + 1)]
    return MVM_rec(S,0, 1, C, M), M

def MVM_rec(S, i, j, C, M):
    if M[i][j] == -math.inf:
        if j >= len(S) - 1 or C == 0:
            M[i][j] = 0
        elif S[j] > C:
            M[i][j] = MVM_rec(S, i, j + 1, C, M)
        else:
            descartar = MVM_rec(S, i, j + 1, C, M)
            incluir = S[j] + MVM_rec(S, j, j + 1, C - S[j], M)
            M[i][j] = max(descartar, incluir)
    return M[i][j]


def MVB(S, C):
    S = [0] + S + [0]
    n = len(S)
    M = [[-math.inf] * n for _ in range(n)]
    for i in range(n-2, -1, -1):
        for j in range(n-1, i, -1):
            if j >= n-1 or C == 0:
                M[i][j] = 0
            else:
                M[i][j] = max(M[i][j+1], S[j] + M[j][j+1])
    return M[0][1], M

def analisis_memoria(S_original, C, M):
    S = [0] + S_original + [0]
    Y = []
    i, j = 0, 1
    L = M[i][j]
    while L > 0:
        if L == M[i][j+1]:
            j += 1
        else:
            Y.append(S[j])
            L -= S[j]
            i = j
            j += 1
    return Y

def MVG(S, C):
    S_sorted = sorted(S, reverse=True)
    total = 0
    seleccion = []
    for v in S_sorted:
        if total + v <= C:
            seleccion.append(v)
            total += v
    return seleccion, total


# Ejemplo de uso
if __name__ == "__main__":
    S = [180, 135, 40, 15]
    C = 300
    resultado, M = greedy_mvm(S, C)
    print("Máximo volumen transportable:", M)