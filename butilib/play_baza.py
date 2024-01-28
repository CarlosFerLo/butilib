from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from .baza import Baza, History
from .card import CardSet
from .contrada import Contrada
from .model import Model
from .schema import PlayInput
from .suit import Suit
from .variants import GameVariant


class PlayBazaInput(BaseModel):
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

    @field_validator("card_sets")
    @classmethod
    def check_all_the_card_sets_are_of_the_same_length(cls, v):
        if all(len(v[i]) == len(v[i + 1]) for i in range(len(v) - 1)):
            return v
        else:
            raise ValueError("Not all the card sets are of the same length.")

    @model_validator(mode="after")
    def check_not_both_butifarra_and_triumph_attributes_are_Set_to_not_none_or_false_values(
        self,
    ):
        if self.triumph is None and self.butifarra == False:
            raise ValueError(
                "Must set one of triumph or butifarra fields to non None/False values."
            )
        if self.triumph is not None and self.butifarra == True:
            raise ValueError(
                "Only one of triumph or butifarra fields can be set to non None/False values."
            )

        return self

    @model_validator(mode="after")
    def check_history_is_consistent(self):
        prev_win = None
        for b in self.history:
            if prev_win is not None:
                if prev_win != b.initial_player:
                    raise ValueError("There is an inconsistency in the history.")
            else:
                called = (
                    self.player_c if not self.delegated else (self.player_c + 2) % 4
                )
                if (called + 1) % 4 != b.initial_player:
                    raise ValueError("There is an inconsistency in the history.")

            if self.butifarra:
                t1 = b.cards[0].suit
                t2 = None
            else:
                t1 = self.triumph
                t2 = b.cards[0].suit

            win_i = 0
            if b.cards[1].compare(b.cards[0], t1, t2):
                win_i = 1

            if b.cards[2].compare(b.cards[win_i], t1, t2):
                win_i = 2

            if b.cards[3].compare(b.cards[win_i], t1, t2):
                win_i = 3

            prev_win = (b.initial_player + win_i) % 4

        if prev_win is not None and prev_win != self.initial_player:
            raise ValueError(
                "The initial_player attribute does not match the winner of the las baza."
            )

        return self

    @model_validator(mode="after")
    def check_the_number_of_bazas_in_history_is_consisten_with_the_number_of_cards_on_card_sets(
        self,
    ):
        if all(12 - len(c) == len(self.history) for c in self.card_sets):
            return self
        else:
            raise ValueError(
                "The number of bazas in the history attribute is inconsistent with the number of cards in a card set."
            )

    @model_validator(mode="after")
    def check_that_there_are_no_repeated_cards(self):
        card_list = []
        for c in self.card_sets:
            card_list.extend(c.cards)
        for b in self.history:
            card_list.extend(b.cards)

        if len(card_list) == len(set(card_list)):
            return self
        else:
            raise ValueError(
                "There are repeated cards between the card sets and/or history."
            )


class PlayBazaOutput(BaseModel):
    baza: Baza


def play_baza(input: PlayBazaInput) -> PlayBazaOutput:
    cards = []

    for i in range(0, 4):
        player_number = (input.initial_player + i) % 4

        play_input = PlayInput(
            history=input.history,
            card_set=input.card_sets[player_number],
            player_number=player_number,
            butifarra=input.butifarra,
            triumph=input.triumph,
            player_c=input.player_c,
            cards=cards,
            delegated=input.delegated,
            game_variant=input.game_variant,
            contrada=input.contrada,
        )

        output = input.players[player_number].play(play_input)
        cards.append(output.card)

    return PlayBazaOutput(baza=Baza(cards=cards, initial_player=input.initial_player))
