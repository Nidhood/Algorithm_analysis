def LIS_with_matrix(S):
    """
    Calcula la longitud de la subsecuencia creciente más larga (LIS) de S
    usando una matriz de memoización M de tamaño (n+1) x (n+2).

    Retorna:
    - best: la longitud de la LIS
    - M: la matriz de memoización llena
    """
    n = len(S)

    # Creamos la matriz M con None para indicar "no calculado"
    #   Filas: 0..n   (usaremos 0..n-1 como índices del arreglo)
    #   Columnas: 1..n+1  (mapeo prev=-1 -> j=1, prev=0 -> j=2, etc.)
    M = [[None] * (n + 2) for _ in range(n + 1)]

    # Llamada inicial: LIS_mem(S, i=0, j=1)
    # j=1 significa "prev = -1" (sin elemento anterior)
    best = LIS_mem(S, 0, 1, M)
    return best, M


def LIS_mem(S, i, j, M):
    """
    Función recursiva con memoización que retorna la longitud de la LIS
    comenzando en índice i, sabiendo que el 'prev' = (j-2).

    - S: arreglo original
    - i: índice actual
    - j: índice del elemento anterior + 2 (para mapear prev=-1 en j=1)
    - M: matriz de memoización
    """
    n = len(S)

    # Si i alcanza el final del arreglo, no hay más elementos que tomar
    if i == n:
        return 0

    # Si ya está calculado, retornamos el valor
    if M[i][j] is not None:
        return M[i][j]

    # Calculamos 'prev' a partir de j
    prev = j - 2  # j=1 -> prev=-1, j=2 -> prev=0, etc.

    # Opción 1: NO tomar S[i]
    ansNoTake = LIS_mem(S, i + 1, j, M)

    # Opción 2: TOMAR S[i] (si arr[i] > arr[prev] o si prev==-1)
    ansTake = 0
    if prev == -1 or S[i] > S[prev]:
        # Al tomar S[i], el nuevo 'prev' pasa a ser i
        #  -> mapeado a j = i+2
        ansTake = 1 + LIS_mem(S, i + 1, i + 2, M)

    # Guardamos el mejor resultado
    M[i][j] = max(ansNoTake, ansTake)
    return M[i][j]


def analizarMemoria(M, S):
    """
    Reconstruye UNA subsecuencia creciente (no necesariamente única) a partir
    de la matriz de memoización M y el arreglo S. Se basa en comparar si
    M[i][j] coincide con "tomar" o "no tomar" S[i].

    Retorna: una lista con los elementos de la subsecuencia elegida.
    """
    subseq = []
    i = 0
    j = 1
    n = len(S)

    while i < n:
        currentVal = M[i][j]
        if currentVal is None:
            # No hay información (caso borde)
            break

        prev = j - 2  # recuperamos el índice previo real

        # Valor si NO tomamos S[i]
        noTakeVal = 0
        if i + 1 <= n:
            # Podría ser None si i+1 == n, así que validamos
            if i + 1 < n and M[i + 1][j] is not None:
                noTakeVal = M[i + 1][j]
            else:
                noTakeVal = 0

        # Valor si TOMAMOS S[i] (si es posible)
        takeVal = float('-inf')
        if prev == -1 or S[i] > S[prev]:
            if i + 1 < n:
                # La parte recursiva de "tomar" es 1 + M[i+1][i+2]
                if M[i + 1][i + 2] is not None:
                    takeVal = 1 + M[i + 1][i + 2]
                else:
                    # Podría ser que i+1 == n-1, etc.
                    takeVal = 1
            else:
                # i == n-1, tomar S[i] da subsecuencia de longitud 1
                takeVal = 1

        # Comparamos con lo que hay en M[i][j]
        if currentVal == takeVal:
            # Significa que "tomamos" S[i]
            subseq.append(S[i])
            j = i + 2  # actualizamos prev a i
            i += 1
        else:
            # No tomamos S[i]
            i += 1

    return subseq


# Ejemplo de uso:
if __name__ == "__main__":
    S = [10, 9, 2, 5, 3, 7, 101, 18]

    best, M = LIS_with_matrix(S)
    print("Longitud de la LIS:", best)

    subsecuencia = analizarMemoria(M, S)
    print("Subsecuencia reconstruida:", subsecuencia)
