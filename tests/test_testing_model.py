import pytest

import butilib


def test_butilib_allows_to_import_test_model_from_the_testing_endpoint():
    from butilib.testing import TestModel


def test_testing_model_is_subclass_of_model():
    from butilib.testing import TestModel

    assert issubclass(TestModel, butilib.Model)


def test_testing_model_accepts_a_card_list_when_instantiated_and_returns_elements_of_it_iteratively():
    from butilib.testing import TestModel

    card_set = butilib.CardSet(
        cards=[
            butilib.Card(number=2, suit=butilib.OROS),
            butilib.Card(number=1, suit=butilib.OROS),
            butilib.Card(number=9, suit=butilib.OROS),
            butilib.Card(number=2, suit=butilib.COPAS),
            butilib.Card(number=5, suit=butilib.BASTOS),
            butilib.Card(number=4, suit=butilib.BASTOS),
            butilib.Card(number=7, suit=butilib.BASTOS),
            butilib.Card(number=10, suit=butilib.BASTOS),
            butilib.Card(number=1, suit=butilib.BASTOS),
            butilib.Card(number=10, suit=butilib.ESPADAS),
            butilib.Card(number=11, suit=butilib.ESPADAS),
            butilib.Card(number=9, suit=butilib.ESPADAS),
        ]
    )

    card_list = [butilib.Card(number=i, suit=butilib.BASTOS) for i in [1, 10, 7]]
    model = TestModel(card_list=card_list)

    play_input = butilib.PlayInput(
        history=butilib.History(bazas=[]),
        card_set=card_set,
        cards=[],
        butifarra=True,
        contrada=butilib.NORMAL,
        player_c=0,
        player_number=1,
        delegated=False,
        game_variant=butilib.LIBRE,
    )

    assert model.card_list == card_list

    for c in card_list:
        output = model._play(play_input)
        assert output.card == c

    for c in card_list:
        output = model.play(play_input)
        assert output.card == c

    output = model.play(play_input)
    assert output.card == card_list[0]
