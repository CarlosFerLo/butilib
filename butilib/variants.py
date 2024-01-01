from enum import Enum

class GameVariant (str, Enum) :
    """ The enum that contains both game variants.
    """
    LIBRE = "LIBRE"
    OBLIGADA = "OBLIGADA"
    
LIBRE = GameVariant.LIBRE
OBLIGADA = GameVariant.OBLIGADA