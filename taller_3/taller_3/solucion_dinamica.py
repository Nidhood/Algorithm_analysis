#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math

# ----------------------------------------
# Top‑Down con memoria
# ----------------------------------------
def top_down(P):
    n = len(P)
    M = [[-math.inf] * (n + 2) for _ in range(n + 1)]
    best = top_down_aux(P, 0, 1, M)
    return best, M

def top_down_aux(P, i, j, M):
    n = len(P)

    # Caso base #1: si hemos sobrepasado el final de la lista,
    # no quedan elementos por procesar => longitud 0
    if i >= n:
        return 0

    # Caso base #2 (memoizacion): si ya calculamos M[i][1],
    # devolvemos el maximo entre ese valor y lo que pueda venir
    # de empezar en i+1 (para propagar el máximo global)
    if M[i][1] != -math.inf:
        return max(M[i][1], top_down_aux(P, i + 1, 1, M))

    # Caso base #3: si i es el ultimo indice, solo cabe
    # un elemento => longitud 1
    if i + 1 >= n:
        length = 1
    else:

        # Caso general: hay al menos un par (P[i], P[i+1])
        d = P[i + 1] - P[i]

        # Si la diferencia es cero, no consideramos variacion => solo P[i]
        if d == 0:
            length = 1
        else:

            # Encontrar cuántos pasos contiguos mantienen la misma d
            length = 1
            k = i
            while k + 1 < n and (P[k+1] - P[k]) == d:
                length += 1
                k += 1

    # Guardar en memoizacion el resultado para i
    M[i][1] = length

    # Combinar: la mejor longitud iniciando en i (length)
    # o la mejor longitud iniciando en i+1 (recursivo)
    return max(length, top_down_aux(P, i + 1, 1, M))

# ----------------------------------------
# Bottom‑Up iterativo
# ----------------------------------------
def bottom_up(P):
    n = len(P)
    M = [[-math.inf] * (n + 2) for _ in range(n + 1)]
    best = 0

    # Rellenar M para cada posible inicio i de la subsecuencia
    for i in range(n - 1):

        # Calculamos la diferencia entre P[i+1] y P[i]
        d = P[i+1] - P[i]

        # Como Minimo podemos contar P[i] solo
        length = 1

        # Caso general: si d != 0, intentar extender mientras siga constante
        if d != 0:
            j = i

            # Mientras los pares contiguos mantengan la misma d
            while j + 1 < n and (P[j+1] - P[j]) == d:
                length += 1
                j += 1

        # Guardamos la longitud máxima encontrada iniciando en i
        M[i][1] = length

        # Actualizamos el best global
        best = max(best, length)

    # Caso base final: si la lista no está vacía, el último elemento
    # solo puede formar una subsecuencia de longitud 1 por sí mismo
    if n > 0:
        M[n-1][1] = 1
        best = max(best, 1)

    # Devolvemos la longitud óptima y la matriz de resultados
    return best, M

# ----------------------------------------
# Analisis de memoria
# ----------------------------------------
def memory_analysis(P, M):
    n = len(P)

    # Buscar la mejor longitud ('best') y su índice de inicio ('start')
    best = -math.inf
    start = 0
    for i in range(n):
        # M[i][1] guarda la longitud de la subsecuencia que arranca en i
        if M[i][1] > best:
            best = M[i][1]
            start = i

    # Si no hay subsecuencia válida (longitud ≤ 0), retornar lista vacía
    if best <= 0:
        return []

    # Calcular fin del slice
    #    la subsecuencia es P[start : start+best],
    #    pero no podemos pasarnos de la longitud de P
    end = min(start + best, n)

    #Devolver el slice contiguo desde 'start' hasta 'end'
    return P[start:end]

if __name__ == "__main__":
    P = [15, 14, 16, 18, 17, 5]

    # Top‑Down
    len_td, M_td = top_down(P)
    seq_td = memory_analysis(P, M_td)
    print(f"Top‑Down: {len_td}, Subsecuencia: {seq_td}")

    # Bottom‑Up
    len_bu, M_bu = bottom_up(P)
    seq_bu = memory_analysis(P, M_bu)
    print(f"Bottom‑Up: {len_bu}, Subsecuencia: {seq_bu}")