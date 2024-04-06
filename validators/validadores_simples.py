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

def count_wall_length(row, ground_characters):
    
    wall_length = 0
    try:
        gap_index = row.index('-')
    except ValueError:
        gap_index = -1
    
    if gap_index == -1:
        return len(row)
    else:
        for char in ground_characters:
            wall_length += row[:gap_index].count(char)
    return wall_length

def read_level_file(file_path):
    """
    Lee el archivo de nivel y lo convierte en una matriz.
    """
    with open(file_path, 'r') as file:
        level_matrix = [line.strip() for line in file]
    return level_matrix

#-----------Validadores fichero txt------------------

def validate_beatable_pit(lvl):

    transpose_matrix = transpose_file(lvl)
    pit_list = []
    non_beatable_pit_count = 0
    row_count = 0

    #Comprobar longitud de los fosos del mapa
    for i, transpose_row in enumerate(transpose_matrix):
        if any(char in GROUND_CHARACTERS for char in transpose_matrix[i - 1]) and set(transpose_row) == {'-'}:
            row_count = 0
        if all(char in NON_WALKABLE_CHARACTERS for char in transpose_row):
            row_count += 1
        if all(char in NON_WALKABLE_CHARACTERS for char in transpose_row) and any(char in GROUND_CHARACTERS for char in transpose_matrix[i + 1]):
            pit_list.append(row_count)

    #Comprobar si alguna de las longitudes es mayor que la distancia de salto de mario
    if all(n <= MAX_HORIZONTAL_JUMP_LENGTH for n in pit_list):
        pass
    else:
        non_beatable_pit_count = sum(1 for n in pit_list if n > MAX_HORIZONTAL_JUMP_LENGTH)

    return non_beatable_pit_count

def validate_beatable_walls(lvl):

    lvl_matrix = read_level_file(lvl)
    lvl_matrix_next_columns = [entry[1:] for entry in lvl_matrix]
    non_beatable_wall_count = 0

    for previous_column, current_column in zip(zip(*lvl_matrix), zip(*lvl_matrix_next_columns)):
        if any(char in GROUND_CHARACTERS for char in current_column):
            current_wall_length = count_wall_length(current_column[::-1], GROUND_CHARACTERS)
            previous_wall_length = count_wall_length(previous_column[::-1], GROUND_CHARACTERS)
            if current_wall_length - previous_wall_length > MAX_VERTICAL_JUMP_LENGTH:
                non_beatable_wall_count += 1

    return non_beatable_wall_count

if __name__== '__main__':

    lvl = 'levels/originals/lvl_2-1.txt'
    print(validate_beatable_walls(lvl))
    
    


