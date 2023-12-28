import pytest
import pydantic
from typing import Callable

import butilib

def test_model_class_inherits_from_pydantic_base_model () :
    assert issubclass(butilib.Model, pydantic.BaseModel)
    
def test_model_has_cantar_method_that_expects_a_cantar_input_and_returns_a_cantar_output () :    
    class MyModel (butilib.Model) :
        def _cantar(self, input: butilib.CantarInput) -> butilib.CantarOutput :
            return butilib.CantarOutput(suit=butilib.OROS)
    
    model = MyModel()
    
    deck = butilib.Deck.new()
    cantar_input = butilib.CantarInput(cards=butilib.CardSet(cards=deck.pop_some(12)), delegated=False)
    
    cantar_output = model.cantar(cantar_input)
    
    assert isinstance(cantar_output, butilib.CantarOutput)
    assert cantar_output.suit == butilib.OROS
    assert cantar_output.delegate == False
    
def test_model_cantar_method_raises_value_error_if_implementation_of_cantar_returns_delegate_in_delegated_call () :
    class MyModel (butilib.Model) :
        def _cantar (self, input) :
            return butilib.CantarOutput(delegate=True)
        
    model = MyModel()
    
    deck = butilib.Deck.new()
    cantar_input = butilib.CantarInput(cards=butilib.CardSet(cards=deck.pop_some(12)), delegated=True)
    
    pytest.raises(ValueError, model.cantar, cantar_input)
    
def test_model_has_contrar_method_that_expects_a_contrar_input_and_returns_a_contrar_output () :
    class MyModel (butilib.Model) :
        def _contrar (self, input: butilib.ContrarInput) -> butilib.ContrarOutput :
            return butilib.ContrarOutput(contrar=False)
        
    model = MyModel()
    
    deck = butilib.Deck.new()
    contrar_input = butilib.ContrarInput(
        cards=butilib.CardSet(cards=deck.pop_some(12)),
        player=1, delegated=False, score=(0, 0), contrada=butilib.NORMAL, triumph=butilib.OROS
    )
    
    output = model.contrar(contrar_input)
    assert isinstance(output, butilib.ContrarOutput)
    assert output.contrar == False

def test_model_has_play_method_that_expects_play_input_and_returns_play_output () :
    class MyModel (butilib.Model) :
        def _play (self, input: butilib.PlayInput) -> butilib.PlayOutput :
            return butilib.PlayOutput(
                card=input.card_set.cards[0]
                )
            
    model = MyModel()
    
    card_set = butilib.CardSet(cards=[
        butilib.Card(number=2, suit=butilib.OROS),
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=9, suit=butilib.OROS),
        
        butilib.Card(number=2, suit=butilib.COPAS),
        butilib.Card(number=5, suit=butilib.COPAS),
        
        butilib.Card(number=4, suit=butilib.BASTOS),
        butilib.Card(number=7, suit=butilib.BASTOS),
        butilib.Card(number=12, suit=butilib.BASTOS),
        butilib.Card(number=1, suit=butilib.BASTOS),
        
        butilib.Card(number=10, suit=butilib.ESPADAS),
        butilib.Card(number=11, suit=butilib.ESPADAS),
        butilib.Card(number=9, suit=butilib.ESPADAS),
    ])
    
    play_input = butilib.PlayInput(
        history=butilib.History(bazas=[]), butifarra=True, player_number=0,
        cards=[], card_set=card_set, contrada=butilib.NORMAL,
        player_c=0, delegated=False,
    )
    
    play_output = model.play(play_input)
    
    assert play_output == butilib.PlayOutput(card=butilib.Card(number=2, suit=butilib.OROS))
    
    play_input = butilib.PlayInput(
        history=butilib.History(bazas=[]), butifarra=True, player_number=0,
        cards=[butilib.Card(number=4, suit=butilib.COPAS)], card_set=card_set, contrada=butilib.NORMAL,
        player_c=0, delegated=False,
    )
    
    assert play_output == butilib.PlayOutput(card=butilib.Card(number=5, suit=butilib.COPAS), forced=True)