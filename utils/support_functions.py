import numpy as np
from project_settings import *
from validators.validadores_simples import transpose_file

def check_column_limit(list, limit):
    """ 
     Check that any number of the list surpasses the limit given
    """
    for number in list:
        if number > limit:
            return False  
    return True  

def euclidean_distance(vec1, vec2):
    """ 
     Calculate the euclidean distance between two given vectors:
     Parametres:
        vec1: numpy array
        vec2: numpy array
    Return:
        distance: float
    """
    diff = vec1 - vec2
    square_diff = np.square(diff)
    sum_square_diff = np.sum(square_diff)
    distance = np.sqrt(sum_square_diff)
    
    return distance

def occurrence_vector(chromosome):
    """
    Calculate the ocurrence of each block in the chromosome
    Parametres:
        chromosome: 1D numpy array
    Return:
        occurrence_vector: 1D numpy array
    """
    occurrence_vector = np.zeros(30, dtype=int)
    for i in chromosome.astype(int):
        occurrence_vector[i] += 1
    return occurrence_vector

# Genetic algorithm reconstruction operators

def rebuild_lvl_pits(lvl):
    """
    Given a level, reduce the length of the pits until they are beatable
    Parametres:
        lvl: str (path to the txt file representing the level)
    Return:
        None
    """
    # Read the level file and calculate the positions to be modified
    with open(lvl, 'r') as file:
        
        pit_list = detect_pits(lvl)
        matrix = [list(line.rstrip()) for line in file]
        print(matrix[0][0])
        
        for pit in pit_list:
            pit_start_index = pit[0]
            pit_length = pit[1]
            pit_start_column = [line[pit_start_index - 1] for line in matrix]
            
            # Find the first ground block before the pit
            indexes = []
            for ground_character in GROUND_CHARACTERS:
                if ground_character in pit_start_column:
                    indexes.append(pit_start_column.index(ground_character))
            floor_index = min(indexes)
            
            
            for i in range(pit_length - MAX_HORIZONTAL_JUMP_LENGTH):
                matrix[floor_index][pit_start_index + i] = 'X'
    
    # Rewrite the modified level
    with open(lvl, 'w') as file:
        for line in matrix:
            file.write(''.join(line) + '\n')

def detect_pits(lvl):
    """
    Detect pits in the level passed as parameter
    Parameters:
        lvl: str (path to the txt file representing the level)
    Return:
        pit_list: list of tuples (position of the pit, length of the pit)
    """

    transpose_matrix = transpose_file(lvl)
    pit_list = []
    row_count = 0
    pit_position = 0

    #Check length of pits on the level
    for i, transpose_row in enumerate(transpose_matrix):
        if any(char in GROUND_CHARACTERS for char in transpose_matrix[i - 1]) and set(transpose_row) == {'-'}:
            row_count = 0
            pit_position = i
        if all(char in NON_WALKABLE_CHARACTERS for char in transpose_row):
            row_count += 1
        if all(char in NON_WALKABLE_CHARACTERS for char in transpose_row) and any(char in GROUND_CHARACTERS for char in transpose_matrix[i + 1]):
            pit_list.append((pit_position, row_count))
            
        long_pits = [pit for pit in pit_list if pit[1] > MAX_HORIZONTAL_JUMP_LENGTH]

    return long_pits

def detect_walls(lvl):
    """
    Detect unbeatable walls in the level passed as parameter
    Parametres:
        lvl: str (path to the txt file representing the level)
    Return:
        wall_list: list of tuples (position of the wall, difference of the vertical position between the wall and previous blocks)
    """
    pass

if __name__ == '__main__':
    rebuild_lvl_pits('levels/originals/pit_lvl_copy.txt')
