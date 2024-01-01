from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional, Tuple, List
from typing_extensions import Annotated
from .card import Card, CardSet
from .baza import History
from .suit import Suit
from .contrada import Contrada, NORMAL, CONTRADA, RECONTRADA, SANT_VICENTADA
from .variants import GameVariant

class CantarInput (BaseModel) :
    """ The input of the cantar method in a model.

        Attributes:
            cards (CardSet): The complete cardset you have.
            delegated (bool): Wether the call wad delegated or not.
            
        Validators:
            validate_cards_has_exactly_12_cards: check wether or not you have a complete card set.
    """
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
    """ The output of the cantar function. It contains the selected suit, butifarra or if you delegate.
    
        Attributes:
            suit (Optional[Suit]): The selected suit or None. Defaults to None.
            delegate (bool): Wether you delegate the call or not. Defaults to False.
            butifarra (bool): Wether you call butifarra or not. Defaults to False.
            
        Validators:
            check_only_one_option_was_set: Check only one of the attributes are set to a non None/False values, but at least one. 
    """
    
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
    """ The input to the contrar function. It contains your cards, your player number, wether the triumph is delegated,
        the selected triumph, current score, and the actual contrada level.
        
        Attributes:
            cards (CardSet): Your cards (should be of length 12).
            player (int): The player number of the one who call triumph (in relation to yours).
            delegated (bool): Wether the triumph was delegated or not.
            triumph (Optional[Suit]): The triumph called. Defaults to None.
            butifarra (bool): If butifarra is called. Defaults to False.
            score (Tuple[int, int]): The current score (your score is the first and theirs the second).
            contrada (Contada): The current level of contrada.
            
        Validators:
            validate_cards_field_contains_a_full_card_set: Check if the card set is full or not.
            check_it_is_possible_to_be_in_that_situation: Check if the conrada level is possible or not.
    """
    
    cards: CardSet
    player: int = Field(ge=0, le=3)
    delegated: bool
    triumph: Optional[Suit] = None
    butifarra: bool = False
    score: Tuple[Annotated[int, Field(ge=0, le=101)], Annotated[int, Field(ge=0, le=101)]]
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
        return self
        
    @model_validator(mode="after")
    def check_only_one_of_triumph_and_butifarra_attributes_is_not_none (self) :
       if self.butifarra is False and self.triumph is None :
           raise ValueError("Only one of suit or butifarra fields can be set to non None/False values.")
       if self.butifarra is True and self.triumph is not None :
            raise ValueError("Must set one of the suit or butifarra fields to non None/False values.")
        
class ContrarOutput (BaseModel) :
    """ The output of the contrar function.

        Attributes:
            contrar (bool): Wether you increment the contrada level or not.
    """
    contrar: bool
    
class PlayInput (BaseModel) :
    """ The input of the play function. It contains the game history, your cards, the triumph suit or butifarra, your player numner,
        the played cards, the contrada level, the player thet contrated, if the call was delegated and the game type.    
    
        Attributes:
            history (History): History of bazas in the game.
            card_set (CardSet): Your card set.
            triumph (Optional[Suit]): The triumph suit or None. Defaults to None.
            butifarra (bool): Wether butifarra was called.
            player_number (int): Your player number (between 0 and 3). 
            cards (List[Card]): The cards played in the current baza.
            contrada (Contrada): The contrada level.
            player_c (int): the player that called triumph (between 0 and 3).
            delegated (bool): wether the call was delegated.
            game_variant (GameType): whether the game variant is LIBREE or OBLIGADA.
            
        Validators:
            check_not_both_butifarra_and_triumph_attributes_are_Set_to_not_none_or_false_values: Check that only one of the butifarra and triumph attributes are not set to non None/False values.
            check_history_is_consistent: Check that the history is consistent within itself and the current baza.
            check_number_of_cards_in_card_set_is_consistent_with_the_number_of_bazas_in_history: Check that you have the correct number of cards.
    """
    history: History
    card_set: CardSet
    triumph: Optional[Suit] = None
    butifarra: bool = False
    player_number: int = Field(ge=0, le=3)
    cards: List[Card]
    contrada: Contrada
    player_c: int = Field(ge=0, le=3)
    delegated: bool
    game_variant: GameVariant
    
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
            
        return self
            
    @model_validator(mode="after")
    def check_number_of_cards_in_card_set_is_consistent_with_the_number_of_bazas_in_history (self) :
        if len(self.card_set) != 12 - len(self.history) :
            raise ValueError(f"The number of cards on the card set is not consistent with the number of bazas in the history. Number of cards: {len(self.card_set)}. Number of bazas: {len(self.history)}.")
        return self

class PlayOutput (BaseModel) :
    """ The output of the play function. This contains the played card and wether it was forced or not.
        A play call is considered forced if only one card is playable and the model is not called.
            
        Attributes:
            card (Card): The card played. 
            forced (bool): Wether the play was forced.
    """
    card: Card
    forced: bool = False