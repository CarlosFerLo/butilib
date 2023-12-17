import pytest
import pydantic

import butilib

def test_deck_class_is_a_pydantic_base_model () :
    assert issubclass(butilib.Deck, pydantic.BaseModel)
    
def test_deck_can_be_init_by_passing_a_list_of_cards () :
    list_of_cards = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=2, suit=butilib.OROS)
    ]
    
    deck = butilib.Deck(cards = list_of_cards)
    
    assert isinstance(deck, butilib.Deck)
    assert deck.cards == list_of_cards
    
def test_deck_can_not_contain_two_identical_cards () :
    list_of_cards = [
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=1, suit=butilib.OROS),
        butilib.Card(number=2, suit=butilib.OROS)
    ]
    
    pytest.raises(pydantic.ValidationError, butilib.Deck, cards=list_of_cards)

def test_deck_has_new_classmethod_that_creates_a_new_instance_of_deck_with_all_the_cards () :
    deck = butilib.Deck.new()
    
    assert isinstance(deck, butilib.Deck)
    
    list_of_cards = []
    for s in butilib.Suit :
        for n in range(1, 13) :
            list_of_cards.append(butilib.Card(number=n, suit=s))
            
    assert deck.cards == list_of_cards
    
def test_deck_has_pop_method_that_returns_a_single_card ():
    deck = butilib.Deck.new()
    
    card = deck.pop()
    assert isinstance(card, butilib.Card)
    assert card == butilib.Card(number=1, suit=butilib.OROS)
    
def test_deck_has_pop_some_method_that_returns_a_list_of_n_cards ():
    deck = butilib.Deck.new()
    
    card_list = deck.pop_some(2)
    assert isinstance(card_list, list)
    assert card_list == [butilib.Card(number=1, suit=butilib.OROS), butilib.Card(number=2, suit=butilib.OROS)]
    
def test_deck_has_shuffle_method_that_randomly_shufles_the_cards_on_the_deck ():
    deck = butilib.Deck.new()
    card_list = deck.cards.copy()
    deck.shuffle()
    
    has_changed = False
    assert len(card_list) == len(deck.cards)
    for c in card_list :
        assert c in deck.cards
        if not has_changed :
            if card_list.index(c) != deck.cards.index(c) :
                has_changed = True
    assert has_changed
    
def test_deck_has_deal_method_that_returns_four_lists_of_cards_and_only_runs_if_the_deck_is_full () :
    deck = butilib.Deck(cards=[])
    pytest.raises(ValueError, deck.deal)
    
    deck = butilib.Deck.new()
    s1, s2, s3, s4 = deck.deal()
    
    assert isinstance(s1, list)
    assert isinstance(s2, list)
    assert isinstance(s3, list)
    assert isinstance(s4, list)
    
    assert len(s1) == 12
    assert len(s2) == 12
    assert len(s3) == 12
    assert len(s4) == 12
    
    assert len([ x for x in s1 if x in s2 ]) == 0
    assert len([ x for x in s1 if x in s3 ]) == 0
    assert len([ x for x in s1 if x in s4 ]) == 0
    assert len([ x for x in s2 if x in s3 ]) == 0
    assert len([ x for x in s2 if x in s4 ]) == 0
    assert len([ x for x in s3 if x in s4 ]) == 0
    
    
    
    
    
    
    
     