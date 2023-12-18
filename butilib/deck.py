from pydantic import BaseModel, field_validator
from typing import List, Tuple
from random import shuffle

from .card import Card, CardSet
from .suit import Suit

class Deck (BaseModel) :
    cards: List[Card]

    @field_validator("cards")
    @classmethod
    def check_that_all_the_cards_in_the_deck_are_different (cls, v) :
        for card in v :
            if v.count(card) > 1 :
                raise ValueError(f"The card: {card} appears more than one in the deck.")
        return v
    
    @classmethod
    def new (cls) :
        card_list = [ Card(number=n, suit=s) for s in Suit for n in range(1, 13) ]
        return cls(
            cards=card_list
        )

    def pop (self) -> Card :
        return self.cards.pop(0)

    def pop_some (self, n: int) -> List[Card] :
        cards = []
        for _ in range(n) :
            cards.append(self.cards.pop(0))
        return cards
    
    def shuffle (self) -> None:
        shuffle(self.cards)
        
    def deal (self) -> Tuple[CardSet, CardSet, CardSet, CardSet] :
        if len(self.cards) != 48 :
            raise ValueError("The deck must be full to use the default deal implementation.")
        
        tup = tuple([CardSet(cards=[]), CardSet(cards=[]), CardSet(cards=[]), CardSet(cards=[])])
        for _ in range(3) :
            for i in range(4) :
                cards = self.pop_some(4)
                tup[i].add(cards)
        
        return tup