import pytest
import pydantic

import butilib


def test_card_object_is_a_pydantic_base_model():
    assert issubclass(butilib.Card, pydantic.BaseModel)


def test_card_object_can_be_init_with_correct_values_of_suit_and_number():
    card = butilib.Card(number=2, suit=butilib.OROS)
    assert isinstance(card, butilib.Card)
    assert card.number == 2
    assert card.suit == butilib.OROS


def test_card_raises_validation_error_if_number_not_in_range_1_to_12():
    pytest.raises(pydantic.ValidationError, butilib.Card, number=0, suit=butilib.OROS)
    pytest.raises(pydantic.ValidationError, butilib.Card, number=13, suit=butilib.OROS)


def test_card_has_points_method_that_returns_the_points_awarded_to_the_team_that_gets_it():
    number_and_points = [
        (9, 5),
        (1, 4),
        (12, 3),
        (11, 2),
        (10, 1),
        (8, 0),
        (7, 0),
        (6, 0),
        (5, 0),
        (4, 0),
        (3, 0),
        (2, 0),
    ]
    for n, p in number_and_points:
        card = butilib.Card(number=n, suit=butilib.OROS)
        assert card.points() == p


def test_card_can_be_compared_for_equality():
    card1 = butilib.Card(number=1, suit=butilib.OROS)
    card2 = butilib.Card(number=1, suit=butilib.OROS)
    card3 = butilib.Card(number=10, suit=butilib.OROS)
    card4 = butilib.Card(number=1, suit=butilib.BASTOS)
    card5 = butilib.Card(number=2, suit=butilib.ESPADAS)

    assert card1 == card2
    assert card1 != card3
    assert card1 != card4
    assert card1 != card5


def test_card_set_is_subclass_of_pydantic_base_model():
    assert issubclass(butilib.CardSet, pydantic.BaseModel)


def test_card_set_can_be_init_from_a_list_of_cards():
    card_list = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=10, suit=butilib.OROS),
        butilib.Card(number=2, suit=butilib.ESPADAS),
    ]
    card_set = butilib.CardSet(cards=card_list)

    assert isinstance(card_set, butilib.CardSet)
    assert card_list == card_set.cards


def test_card_set_can_not_have_repeated_cards():
    card_list = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=10, suit=butilib.OROS),
        butilib.Card(number=2, suit=butilib.ESPADAS),
        butilib.Card(number=10, suit=butilib.OROS),
    ]
    pytest.raises(pydantic.ValidationError, butilib.CardSet, cards=card_list)


def test_card_set_add_method_adds_one_or_more_cards_to_the_set():
    card_list = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=10, suit=butilib.OROS),
    ]
    card_set = butilib.CardSet(cards=card_list)

    assert card_list == card_set.cards

    card_list.append(butilib.Card(number=2, suit=butilib.ESPADAS))
    card_set.add(butilib.Card(number=2, suit=butilib.ESPADAS))

    assert card_list == card_set.cards

    card_extension = [
        butilib.Card(number=10, suit=butilib.OROS),
        butilib.Card(number=10, suit=butilib.BASTOS),
    ]
    card_list.extend(card_extension)
    card_set.add(card_extension)

    assert card_list == card_set.cards


def test_card_set_remove_method_deletes_one_or_more_cards_from_the_set():
    card_list = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=10, suit=butilib.OROS),
        butilib.Card(number=2, suit=butilib.ESPADAS),
        butilib.Card(number=10, suit=butilib.BASTOS),
    ]
    card_set = butilib.CardSet(cards=card_list)

    assert card_list == card_set.cards

    card_list.remove(butilib.Card(number=1, suit=butilib.OROS))
    card_set.remove(butilib.Card(number=1, suit=butilib.OROS))

    assert card_list == card_set.cards

    card_list.remove(butilib.Card(number=10, suit=butilib.OROS))
    card_list.remove(butilib.Card(number=2, suit=butilib.ESPADAS))
    card_set.remove(
        [
            butilib.Card(number=10, suit=butilib.OROS),
            butilib.Card(number=2, suit=butilib.ESPADAS),
        ]
    )

    assert card_list == card_set.cards


def test_card_set_remove_method_raises_value_error_if_try_to_remove_a_card_that_is_not_in_the_set():
    card_list = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=10, suit=butilib.OROS),
        butilib.Card(number=2, suit=butilib.ESPADAS),
        butilib.Card(number=10, suit=butilib.BASTOS),
    ]
    card_set = butilib.CardSet(cards=card_list)

    pytest.raises(
        ValueError, card_set.remove, butilib.Card(number=7, suit=butilib.COPAS)
    )
    pytest.raises(
        ValueError,
        card_set.remove,
        [
            butilib.Card(number=7, suit=butilib.COPAS),
            butilib.Card(number=1, suit=butilib.OROS),
        ],
    )


def test_card_set_points_method_returns_the_sum_of_the_points_of_all_the_inner_cards():
    card_list = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=10, suit=butilib.OROS),
        butilib.Card(number=2, suit=butilib.ESPADAS),
        butilib.Card(number=10, suit=butilib.BASTOS),
    ]
    card_set = butilib.CardSet(cards=card_list)

    assert sum([x.points() for x in card_list]) == card_set.points()


def test_card_set_describe_method_returns_the_correct_description_of_the_card_set():
    card_list = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=10, suit=butilib.OROS),
        butilib.Card(number=2, suit=butilib.ESPADAS),
        butilib.Card(number=10, suit=butilib.BASTOS),
    ]
    card_set = butilib.CardSet(cards=card_list)

    cs_desc = card_set.describe()

    assert cs_desc.oros.number == 2
    assert cs_desc.oros.points == 5
    assert cs_desc.espadas.number == 1
    assert cs_desc.espadas.points == 0
    assert cs_desc.bastos.number == 1
    assert cs_desc.bastos.points == 1
    assert cs_desc.copas.number == 0
    assert cs_desc.copas.points == 0


def test_card_set_has_the_len_dunder_method_implemented_and_returns_the_length_of_the_cards_attribute():
    card_list = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=10, suit=butilib.OROS),
        butilib.Card(number=2, suit=butilib.ESPADAS),
        butilib.Card(number=10, suit=butilib.BASTOS),
    ]
    card_set = butilib.CardSet(cards=card_list)

    assert len(card_list) == len(card_set)


def test_card_set_can_be_an_iterable_of_its_cards():
    card_list = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=10, suit=butilib.OROS),
        butilib.Card(number=2, suit=butilib.ESPADAS),
        butilib.Card(number=10, suit=butilib.BASTOS),
    ]
    card_set = butilib.CardSet(cards=card_list)

    for i, c in enumerate(card_set):
        assert c == card_list[i]

    new_list = [x for x in card_set]
    assert new_list == card_list


def test_card_can_be_converted_to_a_string():
    card = butilib.Card(number=1, suit=butilib.OROS)
    assert str(card) == "1O"

    card = butilib.Card(number=10, suit=butilib.BASTOS)
    assert str(card) == "10B"

    card = butilib.Card(number=2, suit=butilib.ESPADAS)
    assert str(card) == "2E"

    card = butilib.Card(number=12, suit=butilib.COPAS)
    assert str(card) == "12C"


def test_card_is_hashable_and_can_be_added_to_a_set():
    card = butilib.Card(number=1, suit=butilib.OROS)
    h = hash(card)
    assert h is not None

    s = set([card])
    assert len(s) == 1


def test_has_compare_method_that_expects_another_card_and_primary_and_secondary_triumph():
    card1 = butilib.Card(number=1, suit=butilib.OROS)
    card2 = butilib.Card(number=2, suit=butilib.OROS)
    card3 = butilib.Card(number=10, suit=butilib.BASTOS)

    # compare two cards of the same suit
    assert card1.compare(card2, butilib.BASTOS, butilib.OROS)
    assert card2.compare(card2, butilib.ESPADAS)

    # compare cards of different suits depending of the triumphs
    assert not card1.compare(card3, butilib.BASTOS, butilib.OROS)
    assert not card1.compare(card3, butilib.BASTOS)

    assert card2.compare(card3, butilib.COPAS, butilib.ESPADAS)
    assert not card1.compare(card3, butilib.ESPADAS, butilib.BASTOS)


def test_card_set_get_method_accepts_optional_number_and_suit_parameters_and_returns_a_list_of_cards_that_match_provided():
    card_set = butilib.CardSet(
        cards=[
            butilib.Card(number=1, suit=butilib.OROS),
            butilib.Card(number=2, suit=butilib.OROS),
            butilib.Card(number=1, suit=butilib.BASTOS),
        ]
    )

    assert set(card_set.get(number=1)) == set(
        [
            butilib.Card(number=1, suit=butilib.OROS),
            butilib.Card(number=1, suit=butilib.BASTOS),
        ]
    )
    assert set(card_set.get(suit=butilib.OROS)) == set(
        [
            butilib.Card(number=1, suit=butilib.OROS),
            butilib.Card(number=2, suit=butilib.OROS),
        ]
    )
    assert card_set.get(suit=butilib.OROS, number=1) == [
        butilib.Card(number=1, suit=butilib.OROS)
    ]
    assert card_set.get(suit=butilib.ESPADAS) == []


def test_card_set_get_method_raises_an_error_if_no_parameter_is_passed():
    card_set = butilib.CardSet(cards=[])
    pytest.raises(ValueError, card_set.get)


def test_card_set_pop_method_removes_one_random_card_from_the_set():
    card_set = butilib.CardSet(cards=[butilib.Card(number=1, suit=butilib.OROS)])
    card = card_set.pop()

    assert card == butilib.Card(number=1, suit=butilib.OROS)
    assert card_set == butilib.CardSet(cards=[])
