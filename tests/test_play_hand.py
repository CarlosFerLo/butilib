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
    
# TODO: continue implementing all basic validation tests