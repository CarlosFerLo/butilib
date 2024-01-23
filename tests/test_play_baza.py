import pytest
import butilib

import pydantic

def test_play_baza_input_is_a_pydantic_base_model () :
    assert issubclass(butilib.PlayBazaInput, pydantic.BaseModel)
    
def test_play_baza_input_class_has_all_expected_atributes () :
    """PlayBazaInput:
        - history: History
        - players: List[Model] (len == 4)
        - card_sets: List[CardSets] (len == 4)
        - initial_player: int
        - butifarra: bool = False
        - triumph: Optional[Suit] = None
        - player_c: int
        - delegated: bool
        - game_variant: GameVariant
        - contrada: Contrada
    """
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    binput = butilib.PlayBazaInput(
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4], initial_player=0,
        butifarra=True, player_c=3, delegated=False, game_variant=butilib.LIBRE, contrada=butilib.NORMAL
    )
    
    assert binput.history == butilib.History(bazas=[])
    assert binput.players == [m1, m2, m3, m4]
    assert binput.card_sets == [c1, c2, c3, c4]
    assert binput.initial_player == 0
    assert binput.butifarra is True
    assert binput.triumph is None
    assert binput.player_c == 3
    assert binput.delegated is False
    assert binput.contrada == butilib.NORMAL
    
    binput = butilib.PlayBazaInput(
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4], initial_player=0,
        triumph=butilib.OROS, player_c=3, delegated=False, game_variant=butilib.LIBRE, contrada=butilib.NORMAL
    )
    
    assert binput.history == butilib.History(bazas=[])
    assert binput.players == [m1, m2, m3, m4]
    assert binput.card_sets == [c1, c2, c3, c4]
    assert binput.initial_player == 0
    assert binput.butifarra is False
    assert binput.triumph is butilib.OROS
    assert binput.player_c == 3
    assert binput.delegated is False
    assert binput.contrada is butilib.NORMAL
    
def test_play_baza_input_does_not_accept_players_as_a_list_of_more_or_less_than_4_players () :
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    m5 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    pytest.raises(pydantic.ValidationError, butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4, m5], card_sets=[c1, c2, c3, c4], initial_player=0,
        butifarra=True, player_c=3, delegated=False, game_variant=butilib.LIBRE, contrada=butilib.NORMAL
    )
    
    pytest.raises(pydantic.ValidationError, butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3], card_sets=[c1, c2, c3, c4], initial_player=0,
        butifarra=True, player_c=3, delegated=False, game_variant=butilib.LIBRE, contrada=butilib.NORMAL
    )
    
def test_play_baza_input_does_not_accept_card_sets_list_to_be_of_length_different_to_4 () :
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    deck = butilib.Deck.new()
    c5, _, _, _ = deck.deal()
    
    pytest.raises(pydantic.ValidationError, butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4, c5], initial_player=0,
        butifarra=True, player_c=3, delegated=False, game_variant=butilib.LIBRE, contrada=butilib.NORMAL
    )
    
    pytest.raises(pydantic.ValidationError, butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3], initial_player=0,
        butifarra=True, player_c=3, delegated=False, game_variant=butilib.LIBRE, contrada=butilib.NORMAL
    )
    
def test_play_baza_input_does_not_allow_player_numbers_out_of_0_3_range () :
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()
    
    pytest.raises(pydantic.ValidationError, butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4], initial_player=-1,
        butifarra=True, player_c=3, delegated=False, game_variant=butilib.LIBRE, contrada=butilib.NORMAL
    )
    
    pytest.raises(pydantic.ValidationError, butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4], initial_player=4,
        butifarra=True, player_c=3, delegated=False, game_variant=butilib.LIBRE, contrada=butilib.NORMAL
    )
    
    pytest.raises(pydantic.ValidationError, butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4], initial_player=0,
        butifarra=True, player_c=-1, delegated=False, game_variant=butilib.LIBRE, contrada=butilib.NORMAL
    )
    
    pytest.raises(pydantic.ValidationError, butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4], initial_player=0,
        butifarra=True, player_c=4, delegated=False, game_variant=butilib.LIBRE, contrada=butilib.NORMAL
    )