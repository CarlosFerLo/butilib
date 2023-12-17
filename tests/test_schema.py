import pydantic
import pytest
import butilib

def test_cantar_input_is_sublclass_of_pydantic_base_model () :
    assert issubclass(butilib.CantarInput, pydantic.BaseModel)
    
def test_cantar_input_has_cards_and_delegated_fields_and_expects_exactly_twelve_cards () :
    deck = butilib.Deck.new()
    
    card_list = deck.pop_some(12)
    cantar_input = butilib.CantarInput(cards=card_list, delegated=False)
    assert isinstance(cantar_input, butilib.CantarInput)
    assert cantar_input.cards == card_list
    assert cantar_input.delegated == False
    
    card_list = deck.pop_some(6)
    pytest.raises(pydantic.ValidationError, butilib.CantarInput, cards=card_list, delegated=True)
    
    card_list = deck.pop_some(14)
    pytest.raises(pydantic.ValidationError, butilib.CantarInput, cards=card_list, delegated=True)
    
    