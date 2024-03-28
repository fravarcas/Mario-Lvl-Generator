import os
from project_settings import *
import numpy as np

def transpose_file(input_file):
        
    with open(input_file, 'r') as file:
        filas = [line.strip() for line in file.readlines()]

   
    num_filas = len(filas)
    num_columnas = len(filas[0])
    matriz_transpuesta = [''.join(filas[j][i] for j in range(num_filas)) for i in range(num_columnas)]
   
    return matriz_transpuesta

#-----------Validadores fichero txt------------------

def validate_beatable_pit(lvl):

    transpose_matrix = transpose_file(lvl)
    pit_list = []
    non_beatable_pit_count = 0
    row_count = 0

    #Comprobar longitud de los fosos del mapa
    for i, transpose_row in enumerate(transpose_matrix):
        if 'X' in transpose_matrix[i - 1] and set(transpose_row) == {'-'}:
            row_count = 0
        if set(transpose_row) == {'-'}:
            row_count += 1
        if set(transpose_row) == {'-'} and 'X' in transpose_matrix[i + 1]:
            pit_list.append(row_count)

    #Comprobar si alguna de las longitudes es mayor que la distancia de salto de mario
    if all(n <= MAX_HORIZONTAL_JUMP_LENGTH for n in pit_list):
        pass
    else:
        non_beatable_pit_count = sum(1 for n in pit_list if n > MAX_HORIZONTAL_JUMP_LENGTH)

    return non_beatable_pit_count

def validate_beatable_walls(lvl):

    transpose_matrix = transpose_file(lvl)
    non_beatable_wall_count = 0

    for i in range(len(transpose_matrix) - 1):

        if transpose_matrix[i][::-1].find('X') == -1 or transpose_matrix[i + 1][::-1].find('X') == -1:
            pass
        
        else:
            #longitud de la pared en la columna actual
            inverted_row = transpose_matrix[i][::-1]
            find_gap = inverted_row.find('-')
            wall_length = inverted_row[:find_gap].count('X')

            #longitud de la pared en la columna siguiente
            next_inverted_row = ''.join(reversed(transpose_matrix[i + 1]))
            find_next_gap = next_inverted_row.find('-')
            longitud_pared_siguiente = next_inverted_row[:find_next_gap].count('X')

            #Comprueba si la diferencia de longitudes de las paredes es mayor que el salto más alto de mario
            if (wall_length - longitud_pared_siguiente) > MAX_VERTICAL_JUMP_LENGTH:
                non_beatable_wall_count += 1

    return non_beatable_wall_count


