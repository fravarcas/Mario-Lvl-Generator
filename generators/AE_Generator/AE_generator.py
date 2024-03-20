import pygad
import numpy as np
import os
import functools
import operator
from project_settings import *
import random
#from validators.validadores_simples import *

class AEGenerator:
  
  def __init__(self, n_generations, n_parents, sol_per_pop, parent_selection_type, mutation_probability, mutation_by_replacement, lvl_list) -> None:
     
     self.n_generations = n_generations
     self.n_parents = n_parents
     self.sol_per_pop = sol_per_pop
     self.parent_selection_type = parent_selection_type
     self.mutation_probability = mutation_probability
     self.mutation_by_replacement = mutation_by_replacement
     self.lvl_list = lvl_list
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
        
  def decode_matrix(self, matrix, block_codification, output_file):
    
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
        
  def img2chromosome(self, img_arr):

      return np.reshape(a=img_arr, newshape=(functools.reduce(operator.mul, img_arr.shape)))

  def chromosome2img(self, vector, shape):
      # Check if the vector can be reshaped according to the specified shape.
      if len(vector) != functools.reduce(operator.mul, shape):
          raise ValueError("A vector of length {vector_length} into an array of shape {shape}.".format(vector_length=len(vector), shape=shape))

      return np.reshape(a=vector, newshape=shape)
    
  def mutation_function(self, offspring, ga_instance):

      for chromosome_idx in range(offspring.shape[0]):
        for gene in range(offspring.shape[1]):
          if random.random() <= 0.1:
            offspring[chromosome_idx, gene] = random.randint(1, 34)
    
      return offspring
    
  def fitness_function():
    
    pass
    
  def generate_lvl(self) -> None:
    
    #Carga los niveles
    matrix_lvl1_original = self.create_encoded_matrix(self.lvl_list[0], self.block_codification)
    matrix_lvl2_original = self.create_encoded_matrix(self.lvl_list[1], self.block_codification)
    
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
      sol_per_pop=self.sol_per_pop,
      parent_selection_type=self.parent_selection_type,
      mutation_type=self.mutation_function,
      mutation_probability=self.mutation_probability,
      mutation_by_replacement=self.mutation_by_replacement,
      initial_population=initial_pop
      )
    
    

if __name__=='__main__':
  
  current_directory = str(os.getcwd)
  originals_path = os.path.join(current_directory, "..", "levels", "originals")
  lvl_list = [os.path.join(originals_path, "lvl_2-1.txt"), os.path.join(originals_path, "lvl_3-1.txt")]
  
  generador = AEGenerator(
    n_generations=NUMBER_OF_GENERATIONS,
    n_parents=NUMBER_OF_PARENTS,
    sol_per_pop=SOL_PER_POP,
    parent_selection_type=PARENT_SELECTION_TYPE,
    mutation_by_replacement=MUTATION_BY_REPLACEMENT,
    mutation_probability=MUTATION_PROBABILITY,
    lvl_list=lvl_list
    )
  
  generador.generate_lvl()

    
