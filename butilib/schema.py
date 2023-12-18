from pydantic import BaseModel, conlist, model_validator
from typing import Any, Optional, NamedTuple
from .card import Card
from .suit import Suit, OROS, COPAS, BASTOS, ESPADAS

class SuitDescription (NamedTuple) :
    number: int
    points: int

class CardSetDescription (BaseModel) :
    oros: SuitDescription
    bastos: SuitDescription
    copas: SuitDescription
    espadas: SuitDescription
    
    def __getitem__ (self, __key: Suit) -> SuitDescription :
        if __key == OROS :
            return self.oros
        elif __key == BASTOS :
            return self.bastos
        elif __key == COPAS :
            return self.copas
        elif __key == ESPADAS :
            return self.espadas
        else :
            raise KeyError("The only keys of a card set description object are the different suits.")
    def __setitem__ (self, __key: Suit, __value: SuitDescription) -> None :
        if __key == OROS :
            self.oros = __value
        elif __key == BASTOS :
            self.bastos = __value
        elif __key == COPAS :
            self.copas = __value
        elif __key == ESPADAS :
            self.espadas = __value
        else :
            raise KeyError("The only keys of a card set description object are the different suits.")

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
        
class ContrarInput (BaseModel) :
    pass