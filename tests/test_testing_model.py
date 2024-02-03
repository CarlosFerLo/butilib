import pydantic
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


def test_testing_model_accepts_optional_triumph_butifarra_delegate_attributes_that_get_returned_when_the_cantar_method_is_called():
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

    # Check for butifarra True
    model = TestModel(card_list=card_list, butifarra=True)

    assert model.butifarra is True
    assert model.triumph is None
    assert model.delegate is False

    cantar_input = butilib.CantarInput(cards=card_set, delegated=False)

    cantar_output = model.cantar(cantar_input)

    assert cantar_output == butilib.CantarOutput(butifarra=True)

    # Check for not None triumph
    model = TestModel(card_list=card_list, triumph=butilib.OROS)

    assert model.butifarra is False
    assert model.triumph is butilib.OROS
    assert model.delegate is False

    cantar_input = butilib.CantarInput(cards=card_set, delegated=False)

    cantar_output = model.cantar(cantar_input)

    assert cantar_output == butilib.CantarOutput(suit=butilib.OROS)

    # Check for delegate True
    model = TestModel(card_list=card_list, delegate=True)

    assert model.butifarra is False
    assert model.triumph is None
    assert model.delegate is True

    cantar_input = butilib.CantarInput(cards=card_set, delegated=False)

    cantar_output = model.cantar(cantar_input)

    assert cantar_output == butilib.CantarOutput(delegate=True)


def test_testing_model_ensures_that_only_the_butifarra_or_triumph_attributes_are_set_to_not_none_values():
    from butilib.testing import TestModel

    card_list = [butilib.Card(number=i, suit=butilib.BASTOS) for i in [1, 10, 7]]

    pytest.raises(
        pydantic.ValidationError,
        TestModel,
        card_list=card_list,
        butifarra=True,
        triumph=butilib.OROS,
    )


def test_testing_model_accepts_contrada_level_attribute_and_returns_contrar_true_when_calling_contrar_method_if_the_contrada_level_is_lower():
    from butilib.testing import TestModel

    # Test model has contrada level property
    model = TestModel(contrada_level=butilib.NORMAL, card_list=[])

    assert model.contrada_level == butilib.NORMAL

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

    # The model will retrurn true if actual contrada level is lower than the one specified
    model = TestModel(contrada_level=butilib.SANT_VICENTADA, card_list=[])

    contrar_input = butilib.ContrarInput(
        cards=card_set,
        player=1,
        delegated=True,
        butifarra=True,
        score=(1, 10),
        contrada=butilib.NORMAL,
    )

    output = model.contrar(contrar_input)

    assert output == butilib.ContrarOutput(contrar=True)

    # The model will return false if the actual contrada level is equal or higher than the one specified
    model = TestModel(contrada_level=butilib.CONTRADA, card_list=[])

    contrar_input = butilib.ContrarInput(
        cards=card_set,
        player=3,
        delegated=False,
        butifarra=True,
        score=(1, 10),
        contrada=butilib.RECONTRADA,
    )

    output = model.contrar(contrar_input)

    assert output == butilib.ContrarOutput(contrar=False)

    contrar_input = butilib.ContrarInput(
        cards=card_set,
        player=0,
        delegated=False,
        butifarra=True,
        score=(1, 10),
        contrada=butilib.CONTRADA,
    )

    output = model.contrar(contrar_input)

    assert output == butilib.ContrarOutput(contrar=False)
