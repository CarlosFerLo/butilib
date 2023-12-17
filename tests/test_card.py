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