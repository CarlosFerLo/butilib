import pytest
import butilib

from enum import Enum


def test_contrada_is_a_subclass_of_enum_and_has_correct_values():
    assert issubclass(butilib.Contrada, Enum)
    assert butilib.Contrada._member_names_ == [
        "NORMAL",
        "CONTRADA",
        "RECONTRADA",
        "SANT_VICENTADA",
    ]


def test_butilib_allows_for_importing_individual_contrada_values():
    assert butilib.NORMAL == butilib.Contrada.NORMAL
    assert butilib.CONTRADA == butilib.Contrada.CONTRADA
    assert butilib.RECONTRADA == butilib.Contrada.RECONTRADA
    assert butilib.SANT_VICENTADA == butilib.Contrada.SANT_VICENTADA
