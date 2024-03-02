from generators.generador_plano.generator_plain import *
import os
import pytest

@pytest.mark.parametrize("num_rows, num_columns", [(10, 40), (15, 110), (6, 90)])
def test_dummy_generator(tmp_path, num_rows, num_columns):

    test_file = tmp_path / "test_lvl.txt"

    dummy_generator(test_file, num_rows, num_columns)

    assert test_file.exists()

    with open(test_file, 'r') as file:
        content = file.readlines()

        assert len(content) == num_rows
        for row in content:
            assert len(row.strip()) == num_columns

@pytest.mark.parametrize("num_rows, num_columns, pit_position, pit_length", [(10, 40, 10, 8), (15, 110, 30, 15), (6, 90, 50, 10)])
def test_pit_lvl_generator_correct_parametres(tmp_path, num_rows, num_columns, pit_position, pit_length):

    test_file = tmp_path / "test_lvl.txt"

    pit_lvl_generator(test_file, num_rows, num_columns, 2, pit_position, pit_length)

    assert test_file.exists()

    with open(test_file, 'r') as file:
        content = file.readlines()

        assert len(content) == num_rows
        for i, row in enumerate(content):
            assert len(row.strip()) == num_columns
            if i >= num_rows - (2):
                assert row[pit_position] == "-"
                assert row.count("-") == pit_length

@pytest.mark.parametrize("num_rows, num_columns, wall_columns", [(10, 40, [3, 15, 30]), (15, 110, [18, 43, 109]), (6, 90, [1, 3, 10, 20, 50])])
def test_wall_lvl_generator_correct_parametres(tmp_path, num_rows, num_columns, wall_columns):

    test_file = tmp_path / "test_lvl.txt"

    wall_lvl_generator(test_file, num_rows, num_columns, 2, wall_columns)

    assert test_file.exists()

    with open(test_file, 'r') as file:
        content = file.readlines()

        assert len(content) == num_rows
        for row in content:
            assert len(row.strip()) == num_columns
            for column in wall_columns:
                assert row[column] == 'X'
