import os

current_directory = str(os.getcwd)
originals_path = os.path.join(current_directory, "..", "levels", "originals")

def dummy_generator(file_path = os.path.join(originals_path, "lvl_dummy.txt") ,num_rows = 20, num_columns = 200, floor_width = 2):

    #lvl generation
    with open(file_path, 'w') as file:
        grid = ''
        for row in range(num_rows):
            for _ in range(num_columns):
                if row <= num_rows - (floor_width + 1):
                    grid += '-'
                else:
                    grid += 'X'
            grid += '\n'
        file.write(grid)

    return file_path

def pit_lvl_generator(file_path = os.path.join(originals_path, "lvl_foso.txt"), num_rows = 20, num_columns = 200, floor_width = 2, pit_position = 30, pit_length = 13):

    #lvl generation
    with open(file_path, 'w') as file:
        grid = ''
        for row in range(num_rows):
            for column in range(num_columns):
                if row <= num_rows - (floor_width + 1):
                    grid += '-'
                else:
                    grid += 'X' if (column < pit_position or column > pit_position + (pit_length - 1)) else '-' 
            grid += '\n'
        file.write(grid)
    
    return file_path

def wall_lvl_generator(file_path = os.path.join(originals_path, "lvl_pared.txt"), num_rows = 20, num_columns = 200, floor_width = 2, wall_columns = [10, 15, 40, 180]):

    #Generación del nivel
    with open(file_path, 'w') as file:
        grid = ''
        for row in range(num_rows):
            for column in range(num_columns):
                if row <= (num_rows - (floor_width + 1)) and column not in wall_columns:
                    grid += '-'
                else:
                    grid += 'X'
            grid += '\n'
        file.write(grid)
            
    return file_path

if __name__=='__main__':

    wall_lvl_generator(num_columns=100, num_rows=20, floor_width=2)