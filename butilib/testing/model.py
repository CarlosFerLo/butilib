from typing import List, Optional

from pydantic import model_validator

from butilib.card import Card
from butilib.contrada import NORMAL, Contrada
from butilib.model import Model
from butilib.schema import (
    CantarInput,
    CantarOutput,
    ContrarInput,
    ContrarOutput,
    PlayInput,
    PlayOutput,
)
from butilib.suit import Suit


class TestModel(Model):
    card_list: List[Card]

    butifarra: bool = False
    triumph: Optional[Suit] = None
    delegate: bool = False

    contrada_level: Contrada = NORMAL

    _i: int = 0

    __test__ = False

    @model_validator(mode="after")
    def check_only_one_of_the_triumph_or_butifarra_attributes_is_set(self):
        if self.butifarra is True and self.triumph is not None:
            raise ValueError(
                "Only one of the butifarra or triumph attributes can be set to not None/False values."
            )
        else:
            return self

    def _cantar(self, input: CantarInput) -> CantarOutput:
        if self.delegate is True:
            return CantarOutput(delegate=True)

        if self.butifarra is True:
            return CantarOutput(butifarra=True)
        else:
            return CantarOutput(suit=self.triumph)

    def _contrar(self, input: ContrarInput) -> ContrarOutput:
        if input.contrada >= self.contrada_level:
            return ContrarOutput(contrar=False)
        else:
            return ContrarOutput(contrar=True)

    def _play(self, input: PlayInput) -> PlayOutput:
        card = self.card_list[self._i]
        self._i += 1
        self._i %= len(self.card_list)

        return PlayOutput(card=card)
