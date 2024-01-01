from pydantic import BaseModel
from typing import List

from .types import GameType, LIBRE, OBLIGADA
from .schema import CantarInput, CantarOutput, ContrarInput, ContrarOutput, PlayInput, PlayOutput

class Model (BaseModel) :
    game_types: List[GameType] = [ LIBRE, OBLIGADA ]
        
    def cantar (self, input: CantarInput) -> CantarOutput :
        output = self._cantar(input)
        
        if input.delegated and output.delegate :
            raise ValueError("The current implementation of _cantar has returned delegate = True from a delegated call.")
        
        return output
    
    def _cantar (self, input: CantarInput) -> CantarOutput :
        raise NotImplementedError("You should implement _cantar method on a subclass.")
    
    def contrar (self, input: ContrarInput) -> ContrarOutput :
        output = self._contrar(input)
        return output
    
    def _contrar (self, input: ContrarInput) -> ContrarOutput :
        raise NotImplementedError("You should implement _contrar method on a subclass.")
    
    def play (self, input: PlayInput) -> PlayOutput :
        if input.game_type not in self.game_types :
            raise ValueError(f"This model does not support {input.game_type}.")
        
        if input.game_type == LIBRE :
            try :
                output = self._play_libre(input)
            except NotImplementedError :
                output = self._play(input)
        else :
            try :
                output = self._play_obligada(input)
            except NotImplementedError :
                output = self._play(input)
        
        return output
    
    def _play (self, input: PlayInput) -> PlayOutput :
        raise NotImplementedError("You should implement _play method on a subclass.")
    
    def _play_libre (self, input: PlayInput) -> PlayOutput :
        raise NotImplementedError("You should implement _play_libre method on a subclass.")
    
    def _play_obligada (self, input: PlayInput) -> PlayOutput :
        raise NotImplementedError("You should implement _play_obligada method on a subclass.")