from pydantic import BaseModel, conint, field_validator
from typing import List

from .suit import Suit
from .descriptions import CardSetDescription

class Card (BaseModel) :
    number: conint(ge=1, le=12)
    suit: Suit
    
    def points (self) -> int :
         return { 9: 5, 1: 4, 12: 3, 11: 2, 10: 1 }.get(self.number, 0)
     
    def __eq__(self, __value: object) -> bool:
        return self.number == __value.number and self.suit == __value.suit
    
class CardSet (BaseModel) :
    cards: List[Card]
    
    @field_validator("cards")
    @classmethod
    def check_that_all_the_cards_in_the_deck_are_different (cls, v) :
        for card in v :
            if v.count(card) > 1 :
                raise ValueError(f"The card: {card} appears more than one in the card set.")
        return v
        
    def add (self, elem: Card | List[Card]) -> None :
        if isinstance(elem, list) :
            self.cards.extend(elem)
        else :
            self.cards.append(elem)
            
    def remove (self, elem: Card | List[Card]) -> None :
        if isinstance(elem, list) :
            for e in elem :
                self.cards.remove(e)
        else :
            self.cards.remove(elem)
            
    def points (self) -> int :
        return sum([ x.points() for x in self.cards ])
    
    def describe (self) -> CardSetDescription :
        pass