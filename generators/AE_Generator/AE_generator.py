import pygad
import numpy as np
import os
#from validators.validadores_simples import *

block_codification = {
    'M': 1,
    'F': 2,
    'y': 3,
    'Y': 4,
    'E': 5,
    'g': 5,
    'G': 6,
    'k': 7,
    'K': 8,
    'r': 9,
    'X': 10,
    '#': 11,
    '%': 12,
    '|': 13,
    '*': 14,
    'B': 15,
    'b': 16,
    '?': 17,
    '@': 17,
    'Q': 18,
    '!': 19,
    '1': 20,
    '2': 21,
    'D': 22,
    'S': 23,
    'C': 24,
    'U': 25,
    'L': 26,
    'o': 27,
    't': 28,
    'T': 29,
    '<': 30,
    '>': 31,
    '[': 32,
    ']': 33,
    '-': 34
}

def create_encoded_matrix(file_name, encoding):
    
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

            # Get the size of the matrix
            rows = len(lines)
            columns = len(lines[0].strip())

            # Create the encoded matrix
            encoded_matrix = np.zeros((rows, columns), dtype=int)

            # Fill the matrix with the corresponding encoding
            for i in range(rows):
                for j in range(columns):
                    character = lines[i][j]
                    encoded_matrix[i, j] = encoding.get(character, 0)  # 0 if the character is not in the encoding

            return encoded_matrix

    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return None
      
def decode_matrix(matrix, block_codification, output_file):
  
    rows, cols = matrix.shape
    with open(output_file, 'w') as file:
      grid = ''
      for i in range(rows):
        for j in range(cols):
          for key, value in block_codification.items():
            if value == matrix[i, j]:
              grid += key
              break
        grid += '\n'
      file.write(grid)
            
    
def create_initial_population(solutions, n_solutions):
  """
  Creates an initial population for PyGAD by replicating provided solutions equally.

  Args:
    solutions: List of 2D NumPy arrays representing solutions to the problem.
    n_solutions: Total number of solutions desired in the initial population.

  Returns:
    Initial population for PyGAD.
  """

  n_replicas = n_solutions // len(solutions)
  initial_population = []
  for solution in solutions:
    initial_population += [solution] * n_replicas

  # Handling remainder
  if n_solutions % len(solutions) > 0:
    initial_population += solutions[:n_solutions % len(solutions)]

  return initial_population

#def fitness_func(lvl):
    
    #_, num_unbeatable_pits = validate_beatable_pit(lvl)
    #_, num_unbeatable_walls = validate_beatable_walls(lvl)
    #fitness_value = num_unbeatable_pits + num_unbeatable_walls
    
    #return fitness_value

def custom_crossover(parents, crossover_probability):
    
    num_rows, num_cols = parents[0].shape
    crossover_point = np.random.randint(1, num_cols)
    child = np
    
    
    
    
    