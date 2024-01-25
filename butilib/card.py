from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

from .suit import Suit, OROS, BASTOS, COPAS, ESPADAS
from .descriptions import CardSetDescription, SuitDescription

class Card (BaseModel) :
    """ The object representing a card.

        Attributes:
            number (int): The number of the card (from 1 to 12).
            suit (Suit): The suit of the card.
    """
    number: int = Field(ge=1, le=12)
    suit: Suit
    
    def points (self) -> int :
        """ Return the points awarded for having this card at the end of the game.
            9   ->   5
            1   ->   4
            12  ->   3
            11  ->   2
            10  ->   1
            other -> 0

        Returns:
            int: Number of points of that card.
        """
        return { 9: 5, 1: 4, 12: 3, 11: 2, 10: 1 }.get(self.number, 0)
     
    def __eq__(self, __value: object) -> bool:
        """ Check equality among two cards, must have the same number and suit.

        Args:
            __value (object): object to compare the card with, a Card is expected.

        Returns:
            bool: Weather the test was successful.
        """
        return self.number == __value.number and self.suit == __value.suit
    
    def __str__(self) -> str:
        """ Return a stringified verrsion of the card in the following format:
            '{number}{first letter of the suit}'

            Ex: the 9 of OROS is the '90'

        Returns:
            str: string of the card.
        """
        return str(self.number) + { OROS: "O", BASTOS: "B", ESPADAS: "E", COPAS: "C" }[self.suit]
    
    def __hash__(self) -> int:
        """ Hash the card to make it possible to fit on sets. Uses hash function of the stringified version of the card. 

        Returns:
            int: Hash.
        """
        return hash(str(self))
    
    def compare (self, other: "Card", t1: Suit, t2: Optional[Suit] = None) -> bool :
        """ Compare for which of the two cards win. t1 and t2 are the two triumphs, if both are defined, t1 rules over t2.

        Args:
            other (Card): Card to compare against.
            t1 (Suit): First triumph.
            t2 (Optional[Suit], optional): Second triumph. Defaults to None.

        Returns:
            bool: Wether the first card is grater than the second.
        """
        v1 = self.number + self.points() * 100
        v2 = other.number + other.points() * 100
        
        if self.suit not in [t1, t2] and other.suit not in [t1, t2] :
            return True
        
        if self.suit == t1 : v1 += 10000
        elif t2 and self.suit == t2 : v1 += 1000
        
        if other.suit == t1 : v2 += 10000
        elif t2 and other.suit == t2 : v2 += 1000
        
        return v1 >= v2

class CardSet (BaseModel) :
    """ A card set contains an ordered list of cards but has methods for filtering and card set manipulation.

        Attributes :
            cards (List[Card]): List of cards on the card set.
            
        Validators :
            check_that_all_the_cards_in_the_deck_are_different: raise an error if there are repeated cards.
    """
    cards: List[Card]
    
    @field_validator("cards")
    @classmethod
    def check_that_all_the_cards_in_the_deck_are_different (cls, v) :
        for card in v :
            if v.count(card) > 1 :
                raise ValueError(f"The card: {card} appears more than one in the card set.")
        return v
        
    def add (self, elem: Card | List[Card]) -> None :
        """ Add a card or a list of cards to the card set.

        Args:
            elem (Card | List[Card]): The card or list of cards to add to the card set.
        """
        if isinstance(elem, list) :
            self.cards.extend(elem)
        else :
            self.cards.append(elem)
            
    def remove (self, elem: Card | List[Card]) -> None :
        """ Remove a card or list of cards from the card set.

        Args:
            elem (Card | List[Card]): The card or list of cards to remove from the card set.
        """
        if isinstance(elem, list) :
            for e in elem :
                self.cards.remove(e)
        else :
            self.cards.remove(elem)
            
    def points (self) -> int :
        """Count the points on the card set (not taking number of cards into account).

        Returns:
            int: point in the set of cards.
        """
        return sum([ x.points() for x in self.cards ])
    
    def describe (self) -> CardSetDescription :
        """ Generate a description of the card set.

        Returns:
            CardSetDescription: Description of the card set.
        """
        desc = CardSetDescription(
            oros=SuitDescription(number=0, points=0),
            bastos=SuitDescription(number=0, points=0),
            espadas=SuitDescription(number=0, points=0),
            copas=SuitDescription(number=0, points=0),
        )
        
        for c in self.cards :
            desc[c.suit].number = desc[c.suit].number + 1
            desc[c.suit].points = desc[c.suit].points + c.points()
            
        return desc
    
    def __len__ (self) -> int :
        """Return the length of the card sets cards attribute.

        Returns:
            int: length of the card sets cards attribute.
        """
        return len(self.cards)
    
    def __iter__(self) :
        """Return an iterator over the CardSet.
        """
        self._i = 0
        return self
    
    def __next__(self) -> Card:
        """Return the next element in the card set iteration.

        Raises:
            StopIteration: The iteration has finished.

        Returns:
            Card: next card in the iteration.
        """
        try :
            x = self.cards[self._i]
            self._i += 1
            return x
        except IndexError:
            raise StopIteration
        
    def get (self, number: Optional[int] = None, suit: Optional[Suit] = None) -> List[Card] :
        """ Return all the cards that match the specified number and suit filters.

        Args:
            number (Optional[int], optional): The number to search for. Defaults to None.
            suit (Optional[Suit], optional): The suit to search for. Defaults to None.

        Raises:
            ValueError: If no filter is set, an error is raised.add()

        Returns:
            List[Card]: The list of cards on the card set that match the filters.
        """ 
        cards = self.cards
        if number is None and suit is None :
            raise ValueError("At leas one filter must be set to a non None value.")
        if number is not None :
            cards = [ c for c in cards if c.number == number ]
        if suit is not None :
            cards = [ c for c in cards if c.suit == suit ]
            
        return cards
    
    def pop (self) -> Card :
        card = self.cards.pop()
        
        return card