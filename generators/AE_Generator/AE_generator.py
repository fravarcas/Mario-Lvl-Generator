import pygad
import numpy as np
import os
import functools
import operator
from project_settings import *
import random
from validators.validadores_simples import *
import tempfile
from utils.support_functions import euclidean_distance, occurrence_vector, rebuild_lvl_pits, rebuild_lvl_walls

class AEGenerator:
  
  def __init__(self, n_generations, sol_per_pop, parent_selection_type, crossover_type, mutation_probability, mutation_by_replacement, mutation_type, gene_space, lvl_list) -> None:
     
     self.n_generations = n_generations
     self.gene_space = gene_space
     self.sol_per_pop = sol_per_pop
     self.crossover_type = crossover_type
     self.parent_selection_type = parent_selection_type
     self.mutation_probability = mutation_probability
     self.mutation_by_replacement = mutation_by_replacement
     self.mutation_type = mutation_type
     self.lvl_list = lvl_list
     self.matrix_cols = 0
     self.matrix_rows = 0
     self.block_codification = {
          'M': 1,
          'F': 2,
          't': 3,
          'T': 4,
          '|': 5,
          'E': 6,
          'g': 6,
          'G': 7,
          'k': 8,
          'K': 9,
          'r': 10,
          'X': 11,
          '#': 12,
          '%': 13,
          '*': 14,
          'B': 15,
          'b': 16,
          '?': 17,
          '@': 17,
          'Q': 18,
          '!': 18,
          '1': 19,
          '2': 20,
          'D': 21,
          'S': 22,
          'C': 23,
          'U': 24,
          'L': 25,
          'o': 26,
          'y': 27,
          'Y': 28,
          '-': 29
      }

  def create_encoded_matrix(self, file_name, encoding : dict):
      
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

            rows = len(lines)
            columns = len(lines[0].strip())

            encoded_matrix = np.zeros((rows, columns), dtype=int)
            
            for i in range(rows):
                for j in range(columns):
                    character = lines[i][j]
                    encoded_matrix[i, j] = encoding.get(character)

            return encoded_matrix

    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return None
        
  def decode_matrix(self, matrix, block_codification, dir):
    
    rows, cols = matrix.shape
    output_file = os.path.join(dir, 'decoded_matrix.txt')
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
        
    return output_file
        
  def img2chromosome(self, img_arr):

    transposed_arr = np.transpose(img_arr)
    return np.reshape(a=transposed_arr, newshape=(functools.reduce(operator.mul, img_arr.shape)))

  def chromosome2img(self, vector, shape):
    
    if len(vector) != functools.reduce(operator.mul, shape):
      raise ValueError("Cannot reshape a vector of length {vector_length} into an array of shape {shape}.".format(vector_length=len(vector), shape=shape))
    
    # Determine the original shape of the array based on the transposed shape.
    original_shape = tuple(reversed(shape))
    
    return np.transpose(np.reshape(a=vector, newshape=original_shape))
  
  def fitness_function_v2(self, ga_instance, solution, solution_idx):
    
    solution_block_ocurrences = occurrence_vector(solution)
    distance = euclidean_distance(self.original_lvl_occurrences, solution_block_ocurrences)
    if distance <= 30:
      fitness = 1.0 / (1.0 + distance + 90)
    else:
      fitness = 1.0 / (1.0 + distance)
    
    return fitness
    
  def fitness_function(self, ga_instance, solution, solution_idx):
    
    with tempfile.TemporaryDirectory() as temp_dir:
      decoded_solution = self.decode_matrix(self.chromosome2img(solution, (self.matrix_rows, self.matrix_cols)), self.block_codification, temp_dir)
      non_beatable_pits = validate_beatable_pit(decoded_solution)
      non_beatable_walls = validate_beatable_walls(decoded_solution)
    
    non_beatable_elements = non_beatable_pits + non_beatable_walls
    fitness = 1.0 / (1.0 + non_beatable_elements)
    return fitness
    
  def generate_lvl(self) -> None:
    
    #Carga los niveles
    matrix_original_levels = [self.create_encoded_matrix(x, self.block_codification) for x in self.lvl_list]
    
    #Calcula las dimensiones con las que se va a trabajar
    self.matrix_rows = matrix_original_levels[0].shape[0]
    self.matrix_cols = matrix_original_levels[0].shape[1] 
    
    #convierte los niveles a arrays 1D
    matrix_1D_levels = [self.img2chromosome(x) for x in matrix_original_levels]
    self.original_lvl_occurrences = occurrence_vector(matrix_1D_levels[0])
    
    #convierte las matrices que representan los niveles en formato pygad para población inicial
    initial_pop = np.empty((0, len(matrix_1D_levels[0])), dtype=int)
    
    for i in range(self.sol_per_pop):
      
      level_index = i % len(matrix_1D_levels)
      initial_pop = np.vstack((initial_pop, matrix_1D_levels[level_index]))
      
    pop_size = initial_pop.shape[0]
      
    #Crea la instancia pygad
    ga_instance = pygad.GA(
      num_generations=self.n_generations,
      num_parents_mating=pop_size,
      fitness_func=self.fitness_function_v2,
      crossover_type=self.crossover_type,
      parent_selection_type=self.parent_selection_type,
      gene_space=self.gene_space,
      mutation_type=self.mutation_type,
      mutation_probability=self.mutation_probability,
      mutation_by_replacement=self.mutation_by_replacement,
      initial_population=initial_pop,
      )
    
    ga_instance.run()
    solution, _, _ = ga_instance.best_solution()
    solution = self.chromosome2img(solution, (self.matrix_rows, self.matrix_cols))
    self.decode_matrix(solution, self.block_codification, 'levels/generated')
    rebuild_lvl_pits('levels/generated/decoded_matrix.txt')
    rebuild_lvl_walls('levels/generated/decoded_matrix.txt')
    

if __name__=='__main__':
  
  current_directory = str(os.getcwd)
  originals_path = os.path.join(current_directory, "..", "levels", "originals")
  lvl_list = [os.path.join(originals_path, "lvl_2-1.txt"), os.path.join(originals_path, "lvl_3-1.txt"), os.path.join(originals_path, "lvl_4-1.txt")]
  
  generador = AEGenerator(
    n_generations=NUMBER_OF_GENERATIONS,
    sol_per_pop=SOL_PER_POP,
    parent_selection_type=PARENT_SELECTION_TYPE,
    crossover_type=CROSSOVER_TYPE,
    gene_space=GENE_SPACE,
    mutation_type=MUTATION_TYPE,
    mutation_by_replacement=MUTATION_BY_REPLACEMENT,
    mutation_probability=MUTATION_PROBABILITY,
    lvl_list=lvl_list
    )
  
  generador.generate_lvl()

    
