import os
from project_settings import *
import numpy as np

def transpose_file(input_file):
        
    with open(input_file, 'r') as file:
        rows = [line.strip() for line in file.readlines()]

   
    num_rows = len(rows)
    num_columns = len(rows[0])
    transposed_matrix = [''.join(rows[j][i] for j in range(num_rows)) for i in range(num_columns)]
   
    return transposed_matrix

def count_wall_length(column, ground_characters):
    """
    Takes a column of the level and returns the length of the wall in it:
    parametres:
        column: str
        ground_characters: list
    return:
        wall_length: int
    """
    wall_length = 0
    try:
        gap_index = column.index('-')
    except ValueError:
        gap_index = -1
    
    if gap_index == -1:
        return len(column)
    else:
        for char in ground_characters:
            wall_length += column[:gap_index].count(char)
    return wall_length

def read_level_file(file_path):
    """
    Reads level file and transforms it into a matrix
    parametres:
        file_path: str
    return:
        level_matrix: list
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

    #Check length of pits on the level
    for i, transpose_row in enumerate(transpose_matrix):
        if any(char in GROUND_CHARACTERS for char in transpose_matrix[i - 1]) and set(transpose_row) == {'-'}:
            row_count = 0
        if all(char in NON_WALKABLE_CHARACTERS for char in transpose_row):
            row_count += 1
        if all(char in NON_WALKABLE_CHARACTERS for char in transpose_row) and any(char in GROUND_CHARACTERS for char in transpose_matrix[i + 1]):
            pit_list.append(row_count)

    #Check if any of the pits has a length greater than the maximum horizontal jump length of mario
    if all(n <= MAX_HORIZONTAL_JUMP_LENGTH for n in pit_list):
        pass
    else:
        non_beatable_pit_count = sum(1 for n in pit_list if n > MAX_HORIZONTAL_JUMP_LENGTH)

    return non_beatable_pit_count

def validate_beatable_walls(lvl):

    lvl_matrix = read_level_file(lvl)
    lvl_matrix_next_columns = [entry[1:] for entry in lvl_matrix]
    non_beatable_wall_count = 0

    #For each column check if the wall represented by non_walkable blocks of that column is not greater than the last column length by the maximum vertical jump length of mario
    for previous_column, current_column in zip(zip(*lvl_matrix), zip(*lvl_matrix_next_columns)):
        if any(char in GROUND_CHARACTERS for char in current_column):
            current_wall_length = count_wall_length(current_column[::-1], GROUND_CHARACTERS)
            previous_wall_length = count_wall_length(previous_column[::-1], GROUND_CHARACTERS)
            if current_wall_length - previous_wall_length > MAX_VERTICAL_JUMP_LENGTH:
                non_beatable_wall_count += 1

    return non_beatable_wall_count
    
    


