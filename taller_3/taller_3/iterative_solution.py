import math

def calculate_avg_std_iter(numbers):
    # Obtenemos la cantidad de números de la lista
    n = len(numbers)

    # Si la lista está vacía, retornamos 0 para ambos valores
    if n == 0:
        return 0, 0

    # Calculamos el promedio
    sum_numbers = sum(numbers)
    average = sum_numbers / n

    # Calculamos la suma de las diferencias al cuadrado
    sum_squared_diferrences = 0
    for number in numbers:
        diferrence = number - average
        sum_squared_diferrences += diferrence ** 2

    # Calculamos la desviación estándar
    standard_deviation = math.sqrt((sum_squared_diferrences / n))

    # Retornamos el promedio y la desviación estándar
    return average, standard_deviation