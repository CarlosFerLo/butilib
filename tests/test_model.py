import pytest
import pydantic
from typing import List

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
    
def test_model_has_list_of_available_game_variants_as_a_list_of_game_variants_and_deffaults_to_both () :
    model = butilib.Model()
    assert model.game_variants == [ butilib.LIBRE, butilib.OBLIGADA ]
    
    class MyModel (butilib.Model) :
        game_types: List[butilib.GameVariant] = [ butilib.LIBRE ]
        
    my_model = MyModel()
    assert my_model.game_types == [ butilib.LIBRE ]
    
def test_model_has_play_method_that_expects_play_input_and_returns_play_output_calling_auxiliar_call_function () :
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
        player_c=0, delegated=False, game_variant=butilib.LIBRE
    )
    
    play_output = model.play(play_input)
    
    assert play_output == butilib.PlayOutput(card=play_input.card_set.cards[0])
    
def test_model_play_method_raises_value_error_if_model_does_not_allow_that_game_variant () :
    class MyModel (butilib.Model) :
        game_variants: List[butilib.GameVariant] = [butilib.OBLIGADA]
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
        player_c=0, delegated=False, game_variant=butilib.LIBRE
    )
    
    pytest.raises(ValueError, model.play, input=play_input)
    
def test_model_play_method_may_call_call_libre_or_call_obligada_if_defined () :
    class MyModel (butilib.Model) :
        
        def _play (self, input: butilib.PlayInput) -> butilib.PlayOutput :
            return butilib.PlayOutput(
                card=input.card_set.cards[0]
                )
            
        def _play_libre (self, input: butilib.PlayInput) -> butilib.PlayOutput :
            return butilib.PlayOutput(
                card=input.card_set.cards[1]
                )
            
        def _play_obligada (self, input: butilib.PlayInput) -> butilib.PlayOutput :
            return butilib.PlayOutput(
                card=input.card_set.cards[2]
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
        player_c=0, delegated=False, game_variant=butilib.LIBRE
    )
    
    play_output = model.play(play_input)
    assert play_output == butilib.PlayOutput(card=play_input.card_set.cards[1])
    
    play_input = butilib.PlayInput(
        history=butilib.History(bazas=[]), butifarra=True, player_number=0,
        cards=[], card_set=card_set, contrada=butilib.NORMAL,
        player_c=0, delegated=False, game_variant=butilib.OBLIGADA
    )
    
    play_output = model.play(play_input)
    assert play_output == butilib.PlayOutput(card=play_input.card_set.cards[2])
    
    class MyModel (butilib.Model) :
        
        def _play (self, input: butilib.PlayInput) -> butilib.PlayOutput :
            return butilib.PlayOutput(
                card=input.card_set.cards[0]
                )
            
        def _play_libre (self, input: butilib.PlayInput) -> butilib.PlayOutput :
            return butilib.PlayOutput(
                card=input.card_set.cards[1]
                )
             
    model = MyModel()
    
    play_input = butilib.PlayInput(
        history=butilib.History(bazas=[]), butifarra=True, player_number=0,
        cards=[], card_set=card_set, contrada=butilib.NORMAL,
        player_c=0, delegated=False, game_variant=butilib.OBLIGADA
    )
    
    play_output = model.play(play_input)
    assert play_output == butilib.PlayOutput(card=play_input.card_set.cards[0])

def test_model_play_method_returns_forced_true_in_output_if_there_is_only_one_possible_card_to_play_in_obligada () :
    pass