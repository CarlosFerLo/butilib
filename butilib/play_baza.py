from typing import List, Optional
from pydantic import BaseModel, Field

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