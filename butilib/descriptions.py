from pydantic import BaseModel

from .suit import OROS, BASTOS, COPAS, ESPADAS, Suit


class SuitDescription(BaseModel):
    """The description of a suit in a card set. Used as a type for attributes on a CardSetDescription.

    Attributes:
        number (int): number of cards of that suit in the card set.
        points (int): number of points of that suit in the card set.
    """

    number: int
    points: int


class CardSetDescription(BaseModel):
    """Description of the cards in a CardSet.

    Attributes:
        oros (SuitDescription): Description of the OROS suit.
        bastos (SuitDescription): Description of the BASTOS suit.
        copas (SuitDescription): Description of the COPAS suit.
        espadas (SuitDescription): Description of the ESPADAS suit.
    """

    oros: SuitDescription
    bastos: SuitDescription
    copas: SuitDescription
    espadas: SuitDescription

    def __getitem__(self, __key: Suit) -> SuitDescription:
        """Access class attributes as it was a dictionary by providing suits.

        Args:
            __key (Suit): The suit you want to access.

        Raises:
            KeyError: If the input key is not a Suit.

        Returns:
            SuitDescription: The description of the suit.
        """
        if __key == OROS:
            return self.oros
        elif __key == BASTOS:
            return self.bastos
        elif __key == COPAS:
            return self.copas
        elif __key == ESPADAS:
            return self.espadas
        else:
            raise KeyError(
                "The only keys of a card set description object are the different suits."
            )

    def __setitem__(self, __key: Suit, __value: SuitDescription) -> None:
        """Sett the class attributes as it was a dictionary by providing suit.

        Args:
            __key (Suit): The suit you want to change.
            __value (SuitDescription): New SuitDescription

        Raises:
            KeyError: Invalid Suit provided
        """
        if __key == OROS:
            self.oros = __value
        elif __key == BASTOS:
            self.bastos = __value
        elif __key == COPAS:
            self.copas = __value
        elif __key == ESPADAS:
            self.espadas = __value
        else:
            raise KeyError(
                "The only keys of a card set description object are the different suits."
            )
