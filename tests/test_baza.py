import pydantic
import pytest
import butilib

def test_baza_is_a_subclass_of_pydantic_base_model () :
    assert issubclass(butilib.Baza, pydantic.BaseModel)

def test_baza_has_initial_player_played_cards_attributes () :
    baza = butilib.Baza(initial_player=0, cards=[butilib.Card(suit=butilib.OROS, number=1)])
    
    assert isinstance(baza, butilib.Baza)
    assert baza.initial_player == 0
    assert baza.cards == [butilib.Card(suit=butilib.OROS, number=1)]
    
def test_baza_initial_player_is_a_int_between_0_and_3 () :
    pytest.raises(pydantic.ValidationError, butilib.Baza, triumph=butilib.OROS, initial_player=-1, cards=[butilib.Card(suit=butilib.OROS, number=1)])
    pytest.raises(pydantic.ValidationError, butilib.Baza, triumph=butilib.OROS, initial_player=5, cards=[butilib.Card(suit=butilib.OROS, number=1)])
    
def test_baza_cards_has_no_repeated_elements () :
    pytest.raises(pydantic.ValidationError, butilib.Baza, triumph=butilib.OROS, initial_player=0, cards=[butilib.Card(suit=butilib.OROS, number=1), butilib.Card(suit=butilib.OROS, number=1)])

def test_baza_has_add_method_to_add_a_card_to_the_cards_attribute () :
    baza = butilib.Baza(triumph=butilib.OROS, initial_player=0, cards=[])
    baza.add(butilib.Card(number=1, suit=butilib.OROS))
    
    assert baza.cards == [butilib.Card(number=1, suit=butilib.OROS)]
    
