from enum import Enum

import pytest

import butilib


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


def test_contrada_values_can_be_compared_for_ge():
    assert butilib.SANT_VICENTADA >= butilib.SANT_VICENTADA
    assert butilib.SANT_VICENTADA >= butilib.RECONTRADA
    assert butilib.SANT_VICENTADA >= butilib.CONTRADA
    assert butilib.SANT_VICENTADA >= butilib.NORMAL

    assert butilib.RECONTRADA >= butilib.RECONTRADA
    assert butilib.RECONTRADA >= butilib.CONTRADA
    assert butilib.RECONTRADA >= butilib.NORMAL
    assert not butilib.RECONTRADA >= butilib.SANT_VICENTADA

    assert butilib.CONTRADA >= butilib.CONTRADA
    assert butilib.CONTRADA >= butilib.NORMAL
    assert not butilib.CONTRADA >= butilib.RECONTRADA
    assert not butilib.CONTRADA >= butilib.SANT_VICENTADA

    assert butilib.NORMAL >= butilib.NORMAL
    assert not butilib.NORMAL >= butilib.CONTRADA
    assert not butilib.NORMAL >= butilib.RECONTRADA
    assert not butilib.NORMAL >= butilib.SANT_VICENTADA
