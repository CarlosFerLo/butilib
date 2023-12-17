from pydantic import BaseModel, conlist, model_validator
from typing import Optional
from .card import Card
from .suit import Suit

class CantarInput (BaseModel) :
    cards: conlist(Card, max_length=12, min_length=12)
    delegated: bool
    
class CantarOutput (BaseModel) :
    suit: Optional[Suit] = None
    delegate: bool = False
    
    @model_validator(mode="after")
    def check_only_one_option_was_set(self) :
        if self.suit is not None and self.delegate :
            raise ValueError("Not both suit and delegate fields can be set to non None/False values.")
        if self.suit is None and not self.delegate :
            raise ValueError("Must set one of the suit or delegate fields to non None/False values.")