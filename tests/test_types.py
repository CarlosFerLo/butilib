import butilib
import pytest

from enum import Enum

def test_butilib_game_type_enum_has_libre_and_obligada_values ():
    assert issubclass(butilib.GameType, Enum)
    
    assert butilib.GameType._member_names_ == [ "LIBRE", "OBLIGADA" ]
    
def test_butilib_allows_import_of_libre_and_obligada () :
    assert butilib.GameType.LIBRE == butilib.LIBRE
    assert butilib.GameType.OBLIGADA == butilib.OBLIGADA