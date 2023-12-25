from pydantic import BaseModel, conint, field_validator
from typing import List, Optional

from .suit import Suit, OROS, BASTOS, COPAS, ESPADAS
from .descriptions import CardSetDescription, SuitDescription

class Card (BaseModel) :
    number: conint(ge=1, le=12)
    suit: Suit
    
    def points (self) -> int :
         return { 9: 5, 1: 4, 12: 3, 11: 2, 10: 1 }.get(self.number, 0)
     
    def __eq__(self, __value: object) -> bool:
        return self.number == __value.number and self.suit == __value.suit
    
    def __str__(self) -> str:
        return str(self.number) + { OROS: "O", BASTOS: "B", ESPADAS: "E", COPAS: "C" }[self.suit]
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def compare (self, other: "Card", t1: Suit, t2: Optional[Suit] = None) :
        v1 = self.number + self.points() * 100
        v2 = other.number + other.points() * 100
        
        if self.suit not in [t1, t2] and other.suit not in [t1, t2] :
            return True
        
        if self.suit == t1 : v1 += 10000
        elif t2 and self.suit == t2 : v1 += 1000
        
        if other.suit == t1 : v2 += 10000
        elif t2 and other.suit == t2 : v2 += 1000
        
        return v1 >= v2

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
        desc = CardSetDescription(
            oros=SuitDescription(number=0, points=0),
            bastos=SuitDescription(number=0, points=0),
            espadas=SuitDescription(number=0, points=0),
            copas=SuitDescription(number=0, points=0),
        )
        
        for c in self.cards :
            desc[c.suit].number = desc[c.suit].number + 1
            desc[c.suit].points = desc[c.suit].points + c.points()
            
        return desc
    
    def __len__ (self) -> int :
        return len(self.cards)
    
    def __iter__(self) :
        self._i = 0
        return self
    
    def __next__(self) -> Card:
        try :
            x = self.cards[self._i]
            self._i += 1
            return x
        except IndexError:
            raise StopIteration
        