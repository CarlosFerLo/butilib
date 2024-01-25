from typing import List, Tuple
from typing_extensions import Annotated
from pydantic import BaseModel, Field

from butilib.model import Model
from butilib.card import CardSet

class PlayHandInput (BaseModel) :
    players: List[Model] = Field(min_length=4, max_length=4)
    card_sets: List[CardSet] = Field(min_length=4, max_length=4)
    score: Tuple[Annotated[int, Field(ge=0, le=101)], Annotated[int, Field(ge=0, le=101)]]
    player_c: int = Field(ge=0, le=3)