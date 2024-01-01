from pydantic import BaseModel, field_validator
from typing import List, Tuple
from random import shuffle

from .card import Card, CardSet
from .suit import Suit

class Deck (BaseModel) :
    """ A deck of cards, it is used to represent a deck and has useful methods to work with it.
    
        Attributes:
            cards (List[Card]): Cards included in the deck.
            
        Validators:
            check_that_all_the_cards_in_the_deck_are_different: an error is raised if there are two equal cards in the deck.
    """
    cards: List[Card]

    @field_validator("cards")
    @classmethod
    def check_that_all_the_cards_in_the_deck_are_different (cls, v) :
        for card in v :
            if v.count(card) > 1 :
                raise ValueError(f"The card: {card} appears more than one in the deck.")
        return v
    
    @classmethod
    def new (cls) -> "Deck" :
        """ Generate a full deck containing all possible cards, it is ordered.

        Returns:
            Deck: Full deck.
        """
        card_list = [ Card(number=n, suit=s) for s in Suit for n in range(1, 13) ]
        return cls(
            cards=card_list
        )

    def pop (self) -> Card :
        """ Pop the first card of the deck.

        Returns:
            Card: The first card of the deck.
        """
        return self.cards.pop(0)

    def pop_some (self, n: int) -> List[Card] :
        """ Pop the first n cards of the deck.

        Args:
            n (int): Number of cards to pop.

        Returns:
            List[Card]: The first n cards of the deck.
        """
        cards = []
        for _ in range(n) :
            cards.append(self.cards.pop(0))
        return cards
    
    def shuffle (self) -> None:
        """Shuffle the deck inplace.
        """
        shuffle(self.cards)
        
    def deal (self) -> Tuple[CardSet, CardSet, CardSet, CardSet] :
        """ Deal the cards in a full deck. It follows the dealing rules in butifarra: 3 rounds of 4 cards each.

        Raises:
            ValueError: If the deck is not full.

        Returns:
            Tuple[CardSet, CardSet, CardSet, CardSet]: The card sets of the four players.
        """
        if len(self.cards) != 48 :
            raise ValueError("The deck must be full to use the default deal implementation.")
        
        tup = tuple([CardSet(cards=[]), CardSet(cards=[]), CardSet(cards=[]), CardSet(cards=[])])
        for _ in range(3) :
            for i in range(4) :
                cards = self.pop_some(4)
                tup[i].add(cards)
        
        return tup