from pydantic import BaseModel, conlist, conint, model_validator, field_validator
from typing import Optional, Tuple, List
from .card import Card, CardSet
from .baza import History
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
    
class PlayInput (BaseModel) :
    history: History
    card_set: CardSet
    triumph: Optional[Suit] = None
    butifarra: bool = False
    player_number: conint(ge=0, le=3)
    cards: List[Card]
    contrada: Contrada
    player_c: conint(ge=0, le=3)
    delegated: bool
    
    @model_validator(mode="after")
    def check_not_both_butifarra_and_triumph_attributes_are_Set_to_not_none_or_false_values (self) :
        if self.triumph is None and self.butifarra == False :
            raise ValueError("Must set one of triumph or butifarra fields to non None/False values.") 
        if self.triumph is not None and self.butifarra == True :
            raise ValueError("Only one of triumph or butifarra fields can be set to non None/False values.")
        
        return self
        
    @model_validator(mode="after")
    def check_history_is_consistent (self) :
        prev_win = None
        for b in self.history :
            if prev_win is not None :
                if prev_win != b.initial_player :
                    raise ValueError("There is an inconsistency in the history.")
            
            if self.butifarra :
                t1 = b.cards[0].suit
                t2 = None
            else :
                t1 = self.triumph
                t2 = b.cards[0].suit
            
            win_i = 0
            if b.cards[1].compare(b.cards[0], t1, t2) :
                win_i = 1

            if b.cards[2].compare(b.cards[win_i], t1, t2) :
                win_i = 2
                
            if b.cards[3].compare(b.cards[win_i], t1, t2) :
                win_i = 3
                
            prev_win = (b.initial_player + win_i) % 4
            
        if prev_win is not None and len(self.cards) != (self.player_number - prev_win) % 4 :
            raise ValueError("The player_number attribute is not consistent with the cards and history attributes.")
            
            