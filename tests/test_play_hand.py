import pytest
import butilib

import pydantic

def test_play_hand_input_is_a_pydantic_base_model () :
    assert issubclass(butilib.PlayHandInput, pydantic.BaseModel)
    
def test_play_hand_input_has_all_expected_attributes () :
    """PlayHandInput:
        - players: List[Model] (len == 4)
        - card_sets: List[CardSet] (len == 4)
        - score: Tuple[int, int]
        - player_c: int (0 <= n <= 3)
    """
    
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    play_hand_input = butilib.PlayHandInput(
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
        score = (12, 3), player_c=0 
    )
    
    assert isinstance(play_hand_input, butilib.PlayHandInput)
    assert play_hand_input.players == [m1, m2, m3, m4]
    assert play_hand_input.card_sets == [c1, c2, c3, c4]
    assert play_hand_input.score == (12, 3)
    assert play_hand_input.player_c == 0
    
def test_play_hand_input_players_has_fixed_length_of_4_elements () :
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    m5 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3], card_sets=[c1, c2, c3, c4], 
                  score=(12, 3), player_c=0 
                  )
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4, m5], card_sets=[c1, c2, c3, c4], 
                  score=(12, 3), player_c=0 
                  )

def test_play_hand_input_card_sets_has_fixed_length_of_four_elements () :
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3], 
                  score=(12, 3), player_c=0 
                  )
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4, c1], 
                  score=(12, 3), player_c=0 
                  )
def test_play_hand_input_score_is_a_valid_score () :
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
                  score=(-1, 1), player_c=0
                  )
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
                  score=(1, -1), player_c=0
                  )
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
                  score=(102, 1), player_c=0
                  )
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
                  score=(1, 102), player_c=0
                  )
    
def test_play_hand_input_player_c_is_a_number_between_0_and_3 () :
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
                  score=(1, 1), player_c=-1
                  )
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
                  score=(1, 1), player_c=4
                  )
    
def test_play_hand_input_all_card_sets_have_exactly_12_cards () :
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    card = c1.pop()
    
    
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
                  score=(1, 1), player_c=0
                  )
    c1.add(card)
    c2.add(card)
    
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
                  score=(1, 1), player_c=0
                  )
    
def test_play_hand_input_there_are_no_repeated_cards_on_all_the_card_sets ():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    card = c1.pop()
    c2.pop()
    c1.add(card)
    c2.add(card)
    
    pytest.raises(pydantic.ValidationError, butilib.PlayHandInput,
                  players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
                  score=(1, 1), player_c=0
                  )
    
def test_play_hand_output_is_a_pydantic_base_model () :
    assert issubclass(butilib.PlayHandOutput, pydantic.BaseModel)
    
def test_play_hand_output_has_all_expected_attributes () : # TODO
    pass 