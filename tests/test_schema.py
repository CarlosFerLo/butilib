import pydantic
import pytest
import butilib
from typing import NamedTuple

def test_suit_description_is_a_named_tuple_with_atribute_names_number_and_points () :
    suit_description = butilib.SuitDescription(number=8, points=4)
    assert suit_description.number == 8
    assert suit_description.points == 4

def test_card_set_description_inherits_from_pydantic_base_model () :
    assert issubclass(butilib.CardSetDescription, pydantic.BaseModel)
    
def test_card_set_description_has_four_attributes_one_for_each_field_of_type_suit_description () :
    cs_desc = butilib.CardSetDescription(
        oros = butilib.SuitDescription(number=1, points=1),
        bastos = butilib.SuitDescription(number=1, points=1),
        espadas = butilib.SuitDescription(number=1, points=1),
        copas = butilib.SuitDescription(number=1, points=1),
    )
    
    assert isinstance(cs_desc.oros, butilib.SuitDescription)
    assert isinstance(cs_desc.bastos, butilib.SuitDescription)
    assert isinstance(cs_desc.copas, butilib.SuitDescription)
    assert isinstance(cs_desc.espadas, butilib.SuitDescription)
    
    assert cs_desc.oros == butilib.SuitDescription(number=1, points=1)
    assert cs_desc.bastos == butilib.SuitDescription(number=1, points=1)
    assert cs_desc.copas == butilib.SuitDescription(number=1, points=1)
    assert cs_desc.espadas == butilib.SuitDescription(number=1, points=1)
    
def test_card_set_description_attributes_can_be_accessed_as_a_dict () :
    cs_desc = butilib.CardSetDescription(
        oros = butilib.SuitDescription(number=1, points=1),
        bastos = butilib.SuitDescription(number=1, points=1),
        espadas = butilib.SuitDescription(number=1, points=1),
        copas = butilib.SuitDescription(number=1, points=1),
    )
    
    for s in butilib.Suit :
        assert cs_desc[s] == butilib.SuitDescription(number=1, points=1)
        
    with pytest.raises(KeyError) :
        cs_desc["Invalid Key"]
        
def test_card_set_description_attributes_can_be_set_as_a_dict () :
    cs_desc = butilib.CardSetDescription(
        oros = butilib.SuitDescription(number=1, points=1),
        bastos = butilib.SuitDescription(number=1, points=1),
        espadas = butilib.SuitDescription(number=1, points=1),
        copas = butilib.SuitDescription(number=1, points=1),
    )
    
    i = 5
    for s in butilib.Suit :
        cs_desc[s] = butilib.SuitDescription(number=i, points=3)
        assert cs_desc[s] == butilib.SuitDescription(number=i, points=3)
        i += 1 
    
    with pytest.raises(KeyError) :
        cs_desc["Invalid Key"] == butilib.SuitDescription(number=0, points=3)

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