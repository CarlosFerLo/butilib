from pydantic import BaseModel, field_validator, conint, conlist
from typing import List

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
        
class History (BaseModel) :
    bazas: conlist(Baza, max_length=12)
    
    @field_validator("bazas")
    @classmethod
    def validate_bazas_has_no_repeated_cards (cls, v) :
        cards = set([])
        for b in v :
            cards.update(b.cards)
            
        if len(cards) != len(v) * 4 :
            raise ValueError("There are repeated cards in the History.")
        
        return v