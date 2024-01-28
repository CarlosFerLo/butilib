import butilib
import pytest
from enum import Enum


def test_butilib_has_suit_enum_str_with_values_oros_copas_espadas_bastos():
    assert issubclass(butilib.Suit, Enum)
    assert issubclass(butilib.Suit, str)
    assert butilib.Suit._member_names_ == ["OROS", "BASTOS", "ESPADAS", "COPAS"]


def test_butilib_allows_for_importing_individual_suit_values():
    assert butilib.OROS == butilib.Suit.OROS
    assert butilib.COPAS == butilib.Suit.COPAS
    assert butilib.ESPADAS == butilib.Suit.ESPADAS
    assert butilib.BASTOS == butilib.Suit.BASTOS
