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
    
def test_history_is_a_pydantic_base_model () :
    assert issubclass(butilib.History, pydantic.BaseModel)
    
def test_history_has_a_bazas_attribute_that_is_a_list_of_bazas () :
    bazas = [
        butilib.Baza(initial_player=0, cards=[
            butilib.Card(number=1, suit=butilib.OROS),
            butilib.Card(number=2, suit=butilib.OROS),
            butilib.Card(number=3, suit=butilib.OROS),
            butilib.Card(number=4, suit=butilib.OROS)
        ])]
    hystory = butilib.History(bazas=bazas)
    
    assert isinstance(hystory, butilib.History)
    assert hystory.bazas == bazas
    
def test_history_bazas_has_a_number_of_bazas_between_0_to_12 () :
    bazas = []
    for s in butilib.Suit :
        b = [
            butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=s) for i in [9, 1, 12, 11] ]),
            butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=s) for i in [10, 8, 7, 6] ]),
            butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=s) for i in [5, 4, 3, 2] ])
        ]
        bazas.extend(b)
        
    bazas.append(butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.COPAS) for i in [9, 2, 3, 4] ]))
    
    assert len(bazas) == 13
    pytest.raises(pydantic.ValidationError, butilib.History, bazas=bazas)
    
def test_history_checks_that_no_cards_are_repeated_on_the_bazas () :
    pytest.raises(pydantic.ValidationError, butilib.History, bazas =[
        butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.OROS) for i in [1, 2, 3, 4] ]),
        butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.OROS) for i in [2, 5, 6, 7] ])
    ])

def test_history_has_add_method_to_add_a_baza_to_the_end_of_it () :
    history = butilib.History(bazas=[])
    history.add(butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.OROS) for i in [1, 2, 3, 4] ]))
    
    assert history.bazas == [butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.OROS) for i in [1, 2, 3, 4] ])]