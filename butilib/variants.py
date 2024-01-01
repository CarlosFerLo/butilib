from enum import Enum

class GameVariant (Enum) :
    """ The enum that contains both game variants.
    """
    LIBRE = "LIBRE"
    OBLIGADA = "OBLIGADA"
    
LIBRE = GameVariant.LIBRE
OBLIGADA = GameVariant.OBLIGADA