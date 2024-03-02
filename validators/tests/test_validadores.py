import os
from validators.validadores_simples import *

current_directory = os.getcwd()
beatable_wall_file_path = os.path.join(current_directory, "validators", "tests", "test_levels", "lvl_pared_test_beatable.txt")
beatable_pit_file_path = os.path.join(current_directory,  "validators", "tests", "test_levels", "lvl_foso_test_beatable.txt")
unbeatable_pit_file_path = os.path.join(current_directory,  "validators", "tests", "test_levels", "lvl_foso_test_unbeatable.txt")
unbeatable_wall_file_path = os.path.join(current_directory,  "validators", "tests", "test_levels", "lvl_pared_test_unbeatable.txt")

def test_pit_validator():

    assert validar_fosos_pasables(beatable_pit_file_path) == True
    assert validar_fosos_pasables(unbeatable_pit_file_path) == False

def test_wall_validator():

    assert validar_paredes_pasables(beatable_wall_file_path) == True
    assert validar_paredes_pasables(unbeatable_wall_file_path) == False
