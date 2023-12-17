import pytest
import pydantic

import butilib

def test_card_object_is_a_pydantic_base_model ():
    assert issubclass(butilib.Card, pydantic.BaseModel)
    
def test_card_object_can_be_init_with_correct_values_of_suit_and_number () :
    card = butilib.Card(number=2, suit=butilib.OROS)
    assert isinstance(card, butilib.Card)
    assert card.number == 2
    assert card.suit == butilib.OROS
    
def test_card_raises_validation_error_if_number_not_in_range_1_to_12 () :
    pytest.raises(pydantic.ValidationError, butilib.Card, number=0, suit=butilib.OROS)
    pytest.raises(pydantic.ValidationError, butilib.Card, number=13, suit=butilib.OROS)
    
def test_card_has_points_method_that_returns_the_points_awarded_to_the_team_that_gets_it () :
    number_and_points = [(9, 5), (1, 4), (12, 3), (11, 2), (10, 1), (8, 0), (7, 0), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0)]
    for n, p in number_and_points :
        card = butilib.Card(number=n, suit=butilib.OROS)
        assert card.points() == p
        
def test_card_can_be_compared_for_equality () :
    card1 = butilib.Card(number=1, suit=butilib.OROS)
    card2 = butilib.Card(number=1, suit=butilib.OROS)
    card3 = butilib.Card(number=10, suit=butilib.OROS)
    card4 = butilib.Card(number=1, suit=butilib.BASTOS)
    card5 = butilib.Card(number=2, suit=butilib.ESPADAS)
    
    assert card1 == card2
    assert card1 != card3
    assert card1 != card4
    assert card1 != card5