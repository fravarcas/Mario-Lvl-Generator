#Mario properties

MAX_HORIZONTAL_JUMP_LENGTH = 11
MAX_VERTICAL_JUMP_LENGTH= 4

#AE_GEnerator parametres

MUTATION_PROBABILITY = 0.0
NUMBER_OF_GENERATIONS = 50
NUMBER_OF_PARENTS = 2
SOL_PER_POP = 5
CROSSOVER_TYPE = "single_point"
PARENT_SELECTION_TYPE = "random"
MUTATION_BY_REPLACEMENT = True
MUTATION_TYPE = "random"
GENE_SPACE = [x for x in range(1, 35)]

#validator settings

GROUND_CHARACTERS = {'X', '#', 'B', '?', 'Q', '%', 'b', '!', 'D', 'S', 'C', 'U', 'L', 't', 'T'}
NON_WALKABLE_CHARACTERS = {'y', 'Y', 'E', 'g', 'k', 'K', 'r', '|', '1', '2', 'D', '1', '2', 'o', '-'}
