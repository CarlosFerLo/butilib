from enum import Enum
class Suit (str, Enum) :
    """ The enum that contains the values of all the suits.
    """
    OROS = "OROS"
    BASTOS = "BASTOS"
    ESPADAS = "ESPADAS"
    COPAS = "COPAS"
    
OROS = Suit.OROS
COPAS = Suit.COPAS
ESPADAS = Suit.ESPADAS
BASTOS = Suit.BASTOS