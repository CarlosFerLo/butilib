from pydantic import BaseModel, field_validator, model_validator, conint
from typing import List, Optional

from .suit import Suit
from .card import Card

class Baza (BaseModel) :
    triumph: Optional[Suit] = None
    butifarra: bool = False
    initial_player: conint(ge=0, le=3)
    cards: List[Card]
    
    @model_validator(mode="after")
    def check_only_one_option_was_set (self) :
        if self.triumph is not None and self.butifarra :
            raise ValueError("Not both triumph and butifarra fields can be set to non None/False values.")
        if self.triumph is None and not self.butifarra :
            raise ValueError("Must set one of the triumph or butifarra fields to non None/False values.")
        
    @field_validator("cards")
    @classmethod
    def check_cards_has_no_repeated_elements (cls, v) :
        if len(v) != len(set(v)) :
            raise ValueError("Cannot include repeated elements in the cards attribute of a Baza.")
        return v