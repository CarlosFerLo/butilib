from enum import Enum


class Contrada(Enum):
    """An enum representing all the possible contrada levels in a hand.
    Different contrada levels represent different point multipliers.
        NORMAL         ->   x1
        CONTRADA       ->   x2
        RECONTRADA     ->   x4
        SANT_VICENTADA ->   x8
    """

    NORMAL = 0
    CONTRADA = 1
    RECONTRADA = 2
    SANT_VICENTADA = 3

    def __ge__(self, other: "Contrada") -> bool:
        return self.value >= other.value


NORMAL = Contrada.NORMAL
CONTRADA = Contrada.CONTRADA
RECONTRADA = Contrada.RECONTRADA
SANT_VICENTADA = Contrada.SANT_VICENTADA
