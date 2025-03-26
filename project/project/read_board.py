#-------------------------------------------------------------------------
# read_board:   Funcion para leer un archivo con un formato predefifindo
#               para constuir un tablero de juego para FreeFlow
# @inputs   :   Archivo de texto con el formato:
#               num1 ,num2       -> # Numero de filas y columnas respectivamente
#               num1 ,num2 ,num3 -> # Los dos primeros numeros representan la
#                                     coordenada de la celda, y el tercero el
#                                     valor de la celda.
#               (...)            -> # Se repite la estructura anterior para cada celda
# @outputs  :   Clase donde se almacena la matriz del tablero de juego.
# @author   :   Miguel Marquez & Ivan Dario Orozco Ibanez
#-------------------------------------------------------------------------

def read_board(file_name):
    with open(file_name, mode='r') as f:

        (coordenadax, coordenaday, valor)
