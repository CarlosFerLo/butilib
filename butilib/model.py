from pydantic import BaseModel
from typing import List

from .types import GameType, LIBRE, OBLIGADA
from .schema import CantarInput, CantarOutput, ContrarInput, ContrarOutput, PlayInput, PlayOutput

class Model (BaseModel) :
    """ Base Model class of butilib. All deployable models must inherit from this class and implement all desired methods.
        Do not overwrite cantar, contrar or play methods, instead modify the _cantar, _contrar, _play, _play_libre and _play_obligada methods.
        
        Class Attributes:
            game_types (List[GameType]): The supported game types for this model. Defaults to [ butilib.LIBRE, butilib.OBLIGADA ]
    """
    game_types: List[GameType] = [ LIBRE, OBLIGADA ]
        
    def cantar (self, input: CantarInput) -> CantarOutput :
        """ The function called when the model has to select a triumph suit.
            Do not overwrite this method, change the _cantar method instead as this method runs extra checks on the input and output.

        Args:
            input (CantarInput): The input of the cantar function

        Raises:
            ValueError: If the _cantar functions tries to delegate a delegated call.

        Returns:
            CantarOutput: The cantar output.
        """
        output = self._cantar(input)
        
        if input.delegated and output.delegate :
            raise ValueError("The current implementation of _cantar has returned delegate = True from a delegated call.")
        
        return output
    
    def _cantar (self, input: CantarInput) -> CantarOutput :
        """The function you must overwrite to change how the cantar function does.

        Args:
            input (CantarInput): The input of the cantar function

        Raises:
            NotImplementedError: This raises if ypu did not implement the _cantar method in a subclass of butilib.Model

        Returns:
            CantarOutput: The output of the cantar function.
        """
        raise NotImplementedError("You should implement _cantar method on a subclass.")
    
    def contrar (self, input: ContrarInput) -> ContrarOutput :
        """ The function called when the model has to decide weather or not to contrar.
            Do not overwrite this method, change the _contrar method instead as this method runs extra checks on the input and output.

        Args:
            input (ContrarInput): The input of the contrar function

        Returns:
            ContrarOutput: The cantar output.
        """
        output = self._contrar(input)
        return output
    
    def _contrar (self, input: ContrarInput) -> ContrarOutput :
        """The function you must overwrite to change how the contrar function does.

        Args:
            input (ContrarInput): The input of the contrar function

        Raises:
            NotImplementedError: This raises if you did not implement the _contrar method in a subclass of butilib.Model

        Returns:
            ContrarOutput: The output of the contrar function.
        """
        raise NotImplementedError("You should implement _contrar method on a subclass.")
    
    def play (self, input: PlayInput) -> PlayOutput :
        """ The function thet gets called when the model has to decide which card to play.
            Do not overwrite this method, change the _play method instead as this method runs extra checks on the input and output.

        Args:
            input (PlayInput): The input of the play function

        Raises:
            ValueError: If the model does not support this game type.

        Returns:
            PlayOutput: Output of the play function.
        """
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