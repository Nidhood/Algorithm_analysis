"""
#-------------------------------------------------------------------------
# recursive_solution: Recursivamente encuentra el area y las intersecciones de un conjunto de rectangulos, para luego calcular el area total.
# @inputs           : Un conjunto de m rectángulos representado como una secuencia S = ⟨S1, S2, . . . , Sm⟩.
# @outputs          : Un valor entero A ∈ N, donde A = A1 ∪ A2 ∪ A3 ∪ · · · ∪ An y A > 0.
# @author           : Miguel Ángel Márquez Posso
#-------------------------------------------------------------------------
"""

def calcular_interseccion(r1, r2):
    """Calcula el área de intersección entre dos rectángulos."""
    x_izq = max(r1[0][0], r2[0][0])
    x_der = min(r1[1][0], r2[1][0])
    y_arr = min(r1[0][1], r2[0][1])
    y_aba = max(r1[1][1], r2[1][1])

    if x_izq < x_der and y_aba < y_arr:
        return (x_der - x_izq) * (y_arr - y_aba)
    return 0


def calcular_intersecciones(S_izq, S_der):
    """Divide y conquista para calcular las intersecciones entre dos subconjuntos de rectángulos."""
    if not S_izq or not S_der:
        return 0
    if len(S_izq) == 1 and len(S_der) == 1:
        return calcular_interseccion(S_izq[0], S_der[0])

    m1 = len(S_izq) // 2
    m2 = len(S_der) // 2

    A1 = calcular_intersecciones(S_izq[:m1], S_der[:m2])
    A2 = calcular_intersecciones(S_izq[:m1], S_der[m2:])
    A3 = calcular_intersecciones(S_izq[m1:], S_der[:m2])
    A4 = calcular_intersecciones(S_izq[m1:], S_der[m2:])

    return A1 + A2 + A3 + A4


def solucion_divide_vence(S):
    """Resuelve el problema usando la estrategia de dividir y vencer."""
    if not S:
        return 0
    if len(S) == 1:
        (x_u, y_u), (x_d, y_d) = S[0]
        return (x_d - x_u) * (y_u - y_d)

    m = len(S) // 2
    S_izq = S[:m]
    S_der = S[m:]

    A_izq = solucion_divide_vence(S_izq)
    A_der = solucion_divide_vence(S_der)
    A_inter = calcular_intersecciones(S_izq, S_der)

    return A_izq + A_der - A_inter
