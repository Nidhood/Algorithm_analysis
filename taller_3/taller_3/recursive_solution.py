"""
#-------------------------------------------------------------------------
# calculate_avg_std_DYV : Implementa un algoritmo divide y vencerás para calcular el promedio y la desviación estándar de una lista de números.
# @inputs               : Una lista de números, por ejemplo: [1, 2, 3, 4, 5].
# @outputs              : Una tupla (promedio, desviación_estándar) calculados sobre la lista.
# @autor                : Ivan Dario Orozco Ibanez
#-------------------------------------------------------------------------
"""


from math import sqrt

def calculate_avg_std_DYV(numbers):
    return calculate_avg_std_DYV_aux(numbers, 0, len(numbers)-1)

def calculate_avg_std_DYV_aux(numbers, b, e):

    # Caso base (no hay elementos):
    if b > e:
        return 0.0, 0.0

    # Caso base (hay un elemento):
    if b == e:
        return numbers[b], 0.0

    # Caso base (hay dos elementos):
    if e - b == 1:
        avg_partial = (numbers[b] + numbers[e]) / 2
        std_partial = sqrt((pow(numbers[b] - avg_partial, 2) + pow(numbers[e] - avg_partial, 2)) / 2)
        return avg_partial, std_partial

    # Caso recursivo:
    else:
        q = (b + e) // 2
        avg1, s1 = calculate_avg_std_DYV_aux(numbers, b, q)
        avg2, s2 = calculate_avg_std_DYV_aux(numbers, q + 1, e)

        # Numero de elementos en la parte izquierda
        n1 = q - b + 1

        # Numero de elementos en la parte derecha
        n2 = e - q

        # Promedio global:
        avg = (n1 * avg1 + n2 * avg2) / (n1 + n2)

        # Desviación estándar global:
        std = sqrt((n1 * pow(s1, 2) + n2 * pow(s2, 2)) / (n1 + n2) + pow(avg1 - avg2, 2) * n1 * n2 / (pow( (n1 + n2), 2)))
        return avg, std
    # end if