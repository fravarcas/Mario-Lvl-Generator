import os
from validators.validadores_simples import *

current_directory = os.getcwd()
beatable_wall_file_path = os.path.join(current_directory, "validators", "tests", "test_levels", "lvl_pared_test_beatable.txt")
beatable_pit_file_path = os.path.join(current_directory,  "validators", "tests", "test_levels", "lvl_foso_test_beatable.txt")
unbeatable_pit_file_path = os.path.join(current_directory,  "validators", "tests", "test_levels", "lvl_foso_test_unbeatable.txt")
unbeatable_wall_file_path = os.path.join(current_directory,  "validators", "tests", "test_levels", "lvl_pared_test_unbeatable.txt")

def test_pit_validator():

    is_beatable_true, num_unbeatable_pits_true = validate_beatable_pit(beatable_pit_file_path)
    is_beatable_false, num_unbeatable_pits_false = validate_beatable_pit(unbeatable_pit_file_path)

    assert is_beatable_true
    assert num_unbeatable_pits_true == 0
    assert not is_beatable_false
    assert num_unbeatable_pits_false == 3

def test_wall_validator():

    is_beatable_true, num_unbeatable_walls_true = validate_beatable_walls(beatable_wall_file_path)
    is_beatable_false, num_unbeatable_walls_false = validate_beatable_walls(unbeatable_wall_file_path)

    assert is_beatable_true
    assert num_unbeatable_walls_true == 0
    assert not is_beatable_false
    assert num_unbeatable_walls_false == 4
