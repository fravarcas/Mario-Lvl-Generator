import numpy as np

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