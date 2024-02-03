from typing import List, Tuple

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated

from butilib.baza import History
from butilib.card import CardSet
from butilib.contrada import CONTRADA, NORMAL, RECONTRADA, SANT_VICENTADA
from butilib.model import Model
from butilib.schema import CantarInput, ContrarInput


class PlayHandInput(BaseModel):
    players: List[Model] = Field(min_length=4, max_length=4)
    card_sets: List[CardSet] = Field(min_length=4, max_length=4)
    score: Tuple[
        Annotated[int, Field(ge=0, le=101)], Annotated[int, Field(ge=0, le=101)]
    ]
    player_c: int = Field(ge=0, le=3)

    @field_validator("card_sets")
    @classmethod
    def check_card_sets_are_of_length_12(cls, v):
        if all(len(c) == 12 for c in v):
            return v
        else:
            raise ValueError("Not all card sets contain exactly 12 cards.")

    @field_validator("card_sets")
    @classmethod
    def check_card_sets_have_no_repeated_cards(cls, v):
        cards = []
        for c in v:
            cards.extend(c.cards)

        if len(set(cards)) == 48:
            return v
        else:
            raise ValueError("There are duplicate cards between some card sets.")


class PlayHandOutput(BaseModel):
    history: History = Field(min_length=12, max_length=12)


def play_hand(input: PlayHandInput) -> PlayHandOutput:
    # Player_c canta
    player_c = input.player_c
    delegated = False
    cantar_input = CantarInput(cards=input.card_sets[player_c], delegated=delegated)

    output = input.players[player_c].cantar(cantar_input)

    if output.delegate is True:
        player_c = (player_c + 2) % 4
        delegated = True
        cantar_input = CantarInput(cards=input.card_sets[player_c], delegated=delegated)

        output = input.players[player_c].cantar(cantar_input)

    butifarra = output.butifarra
    triumph = output.suit

    # Contrar
    contrada_level = NORMAL
    initial_player = (input.player_c + 1) % 4

    contrar_input = ContrarInput(
        cards=input.card_sets[initial_player],
        player=1 if delegated else 3,
        delegated=delegated,
        butifarra=butifarra,
        triumph=triumph,
        score=input.score,
        contrada=contrada_level,
    )

    output = input.players[initial_player].contrar(contrar_input)

    # TODO: End this implementation
