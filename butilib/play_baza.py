from typing import List, Optional
from pydantic import BaseModel, Field, model_validator

from .suit import Suit
from .contrada import Contrada
from .card import CardSet
from .baza import History
from .model import Model
from .variants import GameVariant


class PlayBazaInput (BaseModel) :
    """PlayBazaInput:
        - history: History
        - players: List[Model] (len == 4)
        - card_sets: List[CardSets] (len == 4)
        - initial_player: int (0 <= n <= 3)
        - butifarra: bool = False
        - triumph: Optional[Suit] = None
        - player_c: int
        - delegated: bool
        - game_variant: GameVariant
        - contrada: Contrada
    """
    history: History
    players: List[Model] = Field(max_length=4, min_length=4)
    card_sets: List[CardSet] = Field(max_length=4, min_length=4)
    initial_player: int = Field(ge=0, le=3)
    butifarra: bool = False
    triumph: Optional[Suit] = None
    player_c: int = Field(ge=0, le=3)
    delegated: bool
    game_variant: GameVariant
    contrada: Contrada
    
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
            else :
                called = self.player_c if not self.delegated else (self.player_c + 2) % 4 
                if (called + 1) % 4 != b.initial_player :
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
            
        if prev_win is not None and prev_win != self.initial_player :
            raise ValueError("The initial_player attribute does not match the winner of the las baza.")
        
        return self
    
    