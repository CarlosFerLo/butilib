from pydantic import BaseModel, field_validator, Field
from typing import List

from .card import Card

class Baza (BaseModel) :
    """ A baza is a the object that represents a baza when playing butifarra. It is mainly included inside a Hystory object.

    Attributes :
        initial_player (int): an int representing the player that started the baza.
        cards (List[Card]): ordered list of cards, in the order played
        
    Validations :
        check_cards_has_no_repeated_elements: checks there are no repeated cards in a baza.
    
    """
    
    initial_player: int = Field(ge=0, le=3)
    cards: List[Card] = Field(max_length=4)
 
    @field_validator("cards")
    @classmethod
    def check_cards_has_no_repeated_elements (cls, v) :
        if len(v) != len(set(v)) :
            raise ValueError("Cannot include repeated elements in the cards attribute of a Baza.")
        return v
    
    def add (self, card: Card) -> None :
        """Add a new card to the baza, it gets appended at the end of the cards attribute.

        Args:
            card (Card): Card to be added.
        """
        self.cards.append(card)
        
    def __eq__(self, __value: object) -> bool:
        """ Compare two cards for equality.

        Args:
            __value (object): Object to be compared with the card, expected to be a Card, otherwise return false.

        Returns:
            bool: Weather equality holds.
        """
        
        if self.initial_player != __value.initial_player :
            return False
        if self.cards != __value.cards :
            return False
        
        return True
class History (BaseModel) :
    """ A set of bazas belonging to the same game, they are stored in an ordered way.

        Attributes:
            bazas (List[Baza]): Ordered list of all the bazas of a game (max 12).
            
        Validators:
            validate_all_bazas_are_complete: make sure all bazas are complete.
            validate_bazas_has_no_repeated_cards: make sure there are no repeated cards among all the bazas in History.
            
    """
    bazas: List[Baza] = Field(max_length=12)
    
    @field_validator("bazas")
    @classmethod
    def validate_all_bazas_are_complete (cls, v) :
        if any([ len(b.cards) < 4 for b in v ]) :
            raise ValueError("THere are incomplete bazas.")
        
        return v
    
    @field_validator("bazas")
    @classmethod
    def validate_bazas_has_no_repeated_cards (cls, v) :
        cards = set([])
        for b in v :
            cards.update(b.cards)
            
        if len(cards) != len(v) * 4 :
            raise ValueError("There are repeated cards in the History.")
        
        return v
    
    def add (self, v: Baza | List[Baza]) -> None :
        """ Add one or more bazas to the end of the bazas attribute.

        Args:
            v (Baza | List[Baza]): Baza or list of bazas to append.
        """
        if isinstance(v, list) :
            self.bazas.extend(v)
        else : 
            self.bazas.append(v)
            
    def __iter__(self) :
        """ Initialize History as an iterator over bazas attribute.
        """
        self._i = 0
        return self
    
    def __next__(self) -> Baza:
        """ Return the next element of the iteration over bazas.

        Raises:
            StopIteration: The iteration has finished, no more elements on bazas.

        Returns:
            Baza: The next baza in bazas.
        """
        try :
            x = self.bazas[self._i]
            self._i += 1
            return x
        except IndexError:
            raise StopIteration
        
    def __eq__(self, __value: object) -> bool:
        """ Check for equality among two history instances.

        Args:
            __value (object): object to check equality against, expected to be of class History

        Returns:
            bool: Weather the vales are equal or not
        """
        return self.bazas == __value.bazas
    
    def __len__(self) -> int :
        """ Get the length of the bazas attribute.

        Returns:
            int: Number of bazas in History.
        """
        return len(self.bazas)