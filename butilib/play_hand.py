from typing import List, Tuple
from typing_extensions import Annotated
from pydantic import BaseModel, Field, field_validator

from butilib.model import Model
from butilib.card import CardSet


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
    pass
