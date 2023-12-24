from pydantic import BaseModel, field_validator, model_validator, conint
from typing import List, Optional

from .suit import Suit
from .card import Card

class Baza (BaseModel) :
    initial_player: conint(ge=0, le=3)
    cards: List[Card]
 
    @field_validator("cards")
    @classmethod
    def check_cards_has_no_repeated_elements (cls, v) :
        if len(v) != len(set(v)) :
            raise ValueError("Cannot include repeated elements in the cards attribute of a Baza.")
        return v
    
    def add (self, card: Card) -> None :
        self.cards.append(card)