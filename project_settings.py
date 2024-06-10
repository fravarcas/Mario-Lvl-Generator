#Mario properties

MAX_HORIZONTAL_JUMP_LENGTH = 9
MAX_VERTICAL_JUMP_LENGTH = 4

#AE_GEnerator standard parametres

MUTATION_PROBABILITY = 0.001
NUMBER_OF_GENERATIONS = 30
SOL_PER_POP = 10
CROSSOVER_TYPE = "single_point"
PARENT_SELECTION_TYPE = "rws"
MUTATION_BY_REPLACEMENT = True
MUTATION_TYPE = "random"
GENE_SPACE = [x for x in range(6, 30)]

#validator settings

GROUND_CHARACTERS = {'X', '#', 'B', '?', 'Q', '%', 'b', '!', 'D', 'S', 'C', 'U', 'L', 't', 'T'}
NON_WALKABLE_CHARACTERS = {'y', 'Y', 'E', 'g', 'k', 'K', 'r', '|', '1', '2', 'D', '1', '2', 'o', '-'}
