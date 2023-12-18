from pydantic import BaseModel, conlist, conint, model_validator, field_validator
from typing import Optional, Tuple
from .card import Card, CardSet
from .suit import Suit
from .contrada import Contrada, NORMAL, CONTRADA, RECONTRADA, SANT_VICENTADA

class CantarInput (BaseModel) :
    cards: CardSet
    delegated: bool
    
    @field_validator("cards")
    @classmethod
    def validate_cards_has_exactly_12_cards (cls, v) :
        if len(v) != 12 :
            raise ValueError("The card set must be of length 12.")
        return v
    
class CantarOutput (BaseModel) :
    suit: Optional[Suit] = None
    delegate: bool = False
    butifarra: bool = False
    
    @model_validator(mode="after")
    def check_only_one_option_was_set(self) :
        if self.suit is not None and self.delegate and self.butifarra :
            raise ValueError("Only one of suit, butifarra and delegate fields can be set to non None/False values.")
        if self.suit is not None and self.delegate :
            raise ValueError("Not both suit and delegate fields can be set to non None/False values.")
        if self.suit is not None and self.butifarra :
            raise ValueError("Not both suit and butifarra fields can be set to non None/False values.")
        if self.butifarra and self.delegate :
            raise ValueError("Not both delegate and butifarra fields can be set to non None/False values.")
        if self.suit is None and not self.delegate and not self.butifarra :
            raise ValueError("Must set one of the suit, delegate or butifarra fields to non None/False values.")
        
class ContrarInput (BaseModel) :
    cards: CardSet
    player: conint(ge=0, le=3)
    delegated: bool
    triumph: Suit
    score: Tuple[conint(ge=0, le=101), conint(ge=0, le=101)]
    contrada: Contrada
    
    @field_validator("cards")
    @classmethod
    def validate_cards_field_contains_a_full_card_set (cls, v) :
        if len(v) != 12 :
            raise ValueError("The card set must be of length 12.")
        return v
    
    @model_validator(mode="after")
    def check_it_is_possible_to_be_in_that_situation (self) :
        if self.contrada == SANT_VICENTADA :
            raise ValueError("Once you have called Sant Vicenç you can no longer continue to contrar.")
        if self.contrada == CONTRADA :
            if self.player % 2 == 1 :
                raise ValueError("This situation cannot be happening in a real game.")
        elif self.player % 2 == 0 :
            raise ValueError("This situation cannot be happening in a real game.")
        
class ContrarOutput (BaseModel) :
    contrar: bool