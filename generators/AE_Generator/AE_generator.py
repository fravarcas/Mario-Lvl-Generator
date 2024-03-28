import pygad
import numpy as np
import os
import functools
import operator
from project_settings import *
import random
from validators.validadores_simples import *
import tempfile

class AEGenerator:
  
  def __init__(self, n_generations, n_parents, sol_per_pop, parent_selection_type, crossover_type, mutation_probability, mutation_by_replacement, mutation_type, gene_space, lvl_list) -> None:
     
     self.n_generations = n_generations
     self.n_parents = n_parents
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

  def create_encoded_matrix(self, file_name, encoding):
      
      try:
          with open(file_name, 'r') as file:
              lines = file.readlines()

              rows = len(lines)
              columns = len(lines[0].strip())

              encoded_matrix = np.zeros((rows, columns), dtype=int)
              
              for i in range(rows):
                  for j in range(columns):
                      character = lines[i][j]
                      encoded_matrix[i, j] = encoding.get(character, 34)  # 34 if the character is not in the encoding

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
    # Check if the vector can be reshaped according to the specified shape.
    if len(vector) != functools.reduce(operator.mul, shape):
        raise ValueError("Cannot reshape a vector of length {vector_length} into an array of shape {shape}.".format(vector_length=len(vector), shape=shape))
    
    # Determine the original shape of the array based on the transposed shape.
    original_shape = tuple(reversed(shape))
    
    return np.transpose(np.reshape(a=vector, newshape=original_shape))
    
  def fitness_function(self, ga_instance, solution, solution_idx):
    
    with tempfile.TemporaryDirectory() as temp_dir:
      decoded_solution = self.decode_matrix(self.chromosome2img(solution, (self.matrix_rows, self.matrix_cols)), self.block_codification, temp_dir)
      non_beatable_pits = validate_beatable_pit(decoded_solution)
      non_beatable_walls = validate_beatable_walls(decoded_solution)
    
    fitness = non_beatable_pits + non_beatable_walls
    return fitness
    
    
  def generate_lvl(self) -> None:
    
    #Carga los niveles
    matrix_lvl1_original = self.create_encoded_matrix(self.lvl_list[0], self.block_codification)
    matrix_lvl2_original = self.create_encoded_matrix(self.lvl_list[1], self.block_codification)
    
    self.matrix_rows = matrix_lvl1_original.shape[0]
    self.matrix_cols = matrix_lvl1_original.shape[1]
    
    #Combierte los niveles a arrays 1D
    matrix_lvl1_1D = self.img2chromosome(matrix_lvl1_original)
    matrix_lvl2_1D = self.img2chromosome(matrix_lvl2_original)
    
    #Combierte las matrices que representan los niveles en formato pygad para población inicial
    initial_pop = np.empty((0, len(matrix_lvl1_1D)), dtype=int)
    
    for _ in range(self.sol_per_pop//2):
      initial_pop = np.vstack((initial_pop, matrix_lvl1_1D))
      
    for _ in range(self.sol_per_pop//2):
      initial_pop = np.vstack((initial_pop, matrix_lvl2_1D))
      
      
    #Crea la instancia pygad
    ga_instance = pygad.GA(
      num_generations=self.n_generations,
      num_parents_mating=self.n_parents,
      fitness_func=self.fitness_function,
      crossover_type=self.crossover_type,
      sol_per_pop=self.sol_per_pop,
      parent_selection_type=self.parent_selection_type,
      gene_space=self.gene_space,
      mutation_type=self.mutation_type,
      mutation_probability=self.mutation_probability,
      mutation_by_replacement=self.mutation_by_replacement,
      initial_population=initial_pop
      )
    
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    solution = self.chromosome2img(solution, (self.matrix_rows, self.matrix_cols))
    print("Best solution : {solution}".format(solution=solution))
    print("Best solution fitness : {solution_fitness}".format(solution_fitness=solution_fitness))
    print("Best solution index : {solution_idx}".format(solution_idx=solution_idx))
    self.decode_matrix(solution, self.block_codification, 'generators/AE_Generator/temp_dir')

if __name__=='__main__':
  
  current_directory = str(os.getcwd)
  originals_path = os.path.join(current_directory, "..", "levels", "originals")
  lvl_list = [os.path.join(originals_path, "lvl_2-1.txt"), os.path.join(originals_path, "lvl_3-1.txt")]
  
  generador = AEGenerator(
    n_generations=NUMBER_OF_GENERATIONS,
    n_parents=NUMBER_OF_PARENTS,
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

    
