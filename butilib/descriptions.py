from pydantic import BaseModel
from typing import NamedTuple

from .suit import OROS, BASTOS, COPAS, ESPADAS, Suit

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
