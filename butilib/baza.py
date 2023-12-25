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
        
    def __eq__(self, __value: object) -> bool:
        if self.initial_player != __value.initial_player :
            return False
        if self.cards != __value.cards :
            return False
        
        return True
class History (BaseModel) :
    bazas: conlist(Baza, max_length=12)
    
    @field_validator("bazas")
    @classmethod
    def validate_all_bazas_are_complete (cls, v) :
        if any([ len(b.cards) < 4 for b in v ]) :
            raise ValueError("THere are incomplete bazas.")
        
        return v
    
    @field_validator("bazas")
    @classmethod
    def validate_bazas_has_no_repeated_cards (cls, v) :
        cards = set([])
        for b in v :
            cards.update(b.cards)
            
        if len(cards) != len(v) * 4 :
            raise ValueError("There are repeated cards in the History.")
        
        return v
    
    def add (self, v: Baza | List[Baza]) -> None :
        if isinstance(v, list) :
            self.bazas.extend(v)
        else : 
            self.bazas.append(v)
            
    def __iter__(self) :
        self._i = 0
        return self
    
    def __next__(self) -> Baza:
        try :
            x = self.bazas[self._i]
            self._i += 1
            return x
        except IndexError:
            raise StopIteration
        
    def __eq__(self, __value: object) -> bool:
        return self.bazas == __value.bazas
    
    def __len__(self) -> int :
        return len(self.bazas)