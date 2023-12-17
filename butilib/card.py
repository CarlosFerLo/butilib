from pydantic import BaseModel, conint

from .schema import Suit

class Card (BaseModel) :
    number: conint(ge=1, le=12)
    suit: Suit
    
    def points (self) -> int :
         return { 9: 5, 1: 4, 12: 3, 11: 2, 10: 1 }.get(self.number, 0)
     
    def __eq__(self, __value: object) -> bool:
        return self.number == __value.number and self.suit == __value.suit