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
    
def test_cantar_output_is_a_subclass_of_pydantic_base_model () :
    assert issubclass(butilib.CantarOutput, pydantic.BaseModel)
    
def test_cantar_output_has_optional_suit_field_and_delegate_field_that_can_not_be_both_set_to_the_same_state () :
    cantar_output = butilib.CantarOutput(suit=butilib.OROS)
    assert isinstance(cantar_output, butilib.CantarOutput)
    assert cantar_output.suit == butilib.OROS
    assert cantar_output.delegate == False
    
    cantar_output = butilib.CantarOutput(delegate=True)
    assert isinstance(cantar_output, butilib.CantarOutput)
    assert cantar_output.suit == None
    assert cantar_output.delegate == True
    
    pytest.raises(pydantic.ValidationError, butilib.CantarOutput, suit=butilib.OROS, delegate=True)
    pytest.raises(pydantic.ValidationError, butilib.CantarOutput)
    
def test_contrar_input_is_a_subclass_of_pydantic_base_model () :
    assert issubclass(butilib.ContrarInput, pydantic.BaseModel)