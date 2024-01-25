from typing import List

from butilib.model import Model
from butilib.card import Card
from butilib.schema import PlayInput, PlayOutput

class TestModel (Model) :
    card_list: List[Card]
    _i = 0
    
    def _play(self, input: PlayInput) -> PlayOutput:
        card = self.card_list[self._i]
        self._i += 1 
        self._i %= len(self.card_list)
        
        return PlayOutput(card=card)