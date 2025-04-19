#!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# read_board:   Funcion para leer un archivo con un formato predefifindo
#               para constuir un tablero de juego para FreeFlow.
# @inputs   :   Archivo de texto con el formato:
#               num1 ,num2       -> # Numero de filas y columnas respectivamente
#               num1 ,num2 ,num3 -> # Los dos primeros numeros representan la
#                                     coordenada de la celda, y el tercero el
#                                     valor de la celda.
#               (...)            -> # Se repite la estructura anterior para cada celda
# @outputs  :   Clase donde se almacena la matriz del tablero de juego.
# @author   :   Miguel Marquez & Ivan Dario Orozco Ibanez.
#-------------------------------------------------------------------------
def read_board(file_name):

    # Primero validamos que exista el archivo y que se pueda leer.
    try:
        with open(file_name, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

    except FileNotFoundError:
        raise FileNotFoundError(f"El fichero '{file_name}' no existe.")

    except IOError as e:
        raise IOError(f"No se pudo leer el fichero '{file_name}': {e}")

    # Luego validamos que la primera linea contenga las dimensiones del tablero (n y m)
    try:
        n_str, m_str = lines[0].split(',')
        n, m = int(n_str), int(m_str)
    except (IndexError, ValueError):
        raise ValueError("La primera línea debe ser 'n,m' con dos enteros separados por coma.")

    # Inicializamos la matriz con ceros
    board = [[0] * m for _ in range(n)]

    # Parseo de las tripletas i,j,v
    for idx, entry in enumerate(lines[1:], start=2):

        # Por ultimo, validamos que cada linea contenga una tripleta i,j,v
        try:
            i_str, j_str, v_str = entry.split(',')
            i, j, v = int(i_str), int(j_str), int(v_str)
            if not (1 <= i <= n and 1 <= j <= m):
                raise IndexError(f"Coordenada fuera de rango en línea {idx}: ({i},{j})")
            board[i - 1][j - 1] = v
        except ValueError:
            raise ValueError(f"Línea {idx} mal formateada (se esperaban tres enteros): '{entry}'")
        except IndexError as e:
            raise IndexError(f"Error en línea {idx}: {e}")
    return board