#!/usr/bin/python3
# -*- coding: utf-8 -*-
from project.free_flow.board.read_board import read_board
from project.free_flow.game.start import start
from project.free_flow.graph.graph import Graph
#-------------------------------------------------------------------------
# free_flow :   Juego que consiste en conectar numeros en parejas de dos, ubicados 
#               en un tablero de nxn celdas. La unica restriccion es que se deben 
#               conectar todos los numeros sin cruzar lineas entre si
# @inputs   :   Tablero de nxn celdas con parejas de numeros enteros positivos.
# @outputs  :   Valor booleano que indica si el jugador/maquina logro conectar
#               todos los numeros sin cruzar lineas entre si.
# @author   :   Miguel & Ivan Dario Orozco Ibanez
#-------------------------------------------------------------------------
def free_flow(board_file):
    # Pasos que debe cumplir el algoritmo:

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    # 1. Leer el archivo de entrada, con el siguiente formato:
    # 7 ,7      -> # Numero de filas y columnas respectivamente
    # 1 ,4 ,4   -> # Los dos primeros numeros representan la coordenada de la celda, y el tercero el valor de la celda
    # 2 ,2 ,3   -> # Los dos primeros numeros representan la coordenada de la celda, y el tercero el valor de la celda
    # 2 ,5 ,2   -> # Los dos primeros numeros representan la coordenada de la celda, y el tercero el valor de la celda
    # 2 ,6 ,5   -> # Los dos primeros numeros representan la coordenada de la celda, y el tercero el valor de la celda
    # 3 ,4 ,3   -> # Los dos primeros numeros representan la coordenada de la celda, y el tercero el valor de la celda
    # 3 ,5 ,1   -> # Los dos primeros numeros representan la coordenada de la celda, y el tercero el valor de la celda
    # 4 ,4 ,5   -> # Los dos primeros numeros representan la coordenada de la celda, y el tercero el valor de la celda
    # 6 ,3 ,1   -> # Los dos primeros numeros representan la coordenada de la celda, y el tercero el valor de la celda
    # 7 ,1 ,2   -> # Los dos primeros numeros representan la coordenada de la celda, y el tercero el valor de la celda
    # 7 ,5 ,4   -> # Los dos primeros numeros representan la coordenada de la celda, y el tercero el valor de la celda
    input_board = read_board(board_file)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # 3. Crear un grafo a partir del tablero de nxn celdas.
    graph = Graph(input_board)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # 4. Iniciar juego:
    start(graph)