from pydantic import BaseModel

from .schema import CantarInput, CantarOutput

class Model (BaseModel) :
    def cantar (self, input: CantarInput) -> CantarOutput :
        output = self._cantar(input)
        
        if input.delegated and output.delegate :
            raise ValueError("The current implementation of _cantar has returned delegate = True from a delegated call.")
        
        return output
    
    def _cantar (self, input: CantarInput) -> CantarOutput :
        raise NotImplementedError("You should implement _cantar method on a subclass.")
    
    