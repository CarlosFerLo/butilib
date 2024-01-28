from enum import Enum

import pytest

import butilib


def test_butilib_game_type_enum_str_has_libre_and_obligada_values():
    assert issubclass(butilib.GameVariant, Enum)
    assert issubclass(butilib.GameVariant, str)

    assert butilib.GameVariant._member_names_ == ["LIBRE", "OBLIGADA"]


def test_butilib_allows_import_of_libre_and_obligada():
    assert butilib.GameVariant.LIBRE == butilib.LIBRE
    assert butilib.GameVariant.OBLIGADA == butilib.OBLIGADA
