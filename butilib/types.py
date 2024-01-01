from enum import Enum

class GameType (Enum) :
    """ The enum that contains both game variants.
    """
    LIBRE = "LIBRE"
    OBLIGADA = "OBLIGADA"
    
LIBRE = GameType.LIBRE
OBLIGADA = GameType.OBLIGADA