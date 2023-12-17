import pytest
import pydantic
from typing import Callable

import butilib

def test_model_class_inherits_from_pydantic_base_model () :
    assert issubclass(butilib.Model, pydantic.BaseModel)
    
def test_model_has_cantar_method_that_expects_a_cantar_input_and_returns_a_cantar_input () :    
    class MyModel (butilib.Model) :
        def _cantar(self, input: butilib.CantarInput) -> butilib.CantarOutput :
            return butilib.CantarOutput(suit=butilib.OROS)
    
    model = MyModel()
    
    deck = butilib.Deck.new()
    cantar_input = butilib.CantarInput(cards=deck.pop_some(12), delegated=False)
    
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
    cantar_input = butilib.CantarInput(cards=deck.pop_some(12), delegated=True)
    
    pytest.raises(ValueError, model.cantar, cantar_input)