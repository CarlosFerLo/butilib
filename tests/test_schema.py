import pydantic
import pytest
import butilib


def test_cantar_input_is_sublclass_of_pydantic_base_model () :
    assert issubclass(butilib.CantarInput, pydantic.BaseModel)
    
def test_cantar_input_has_cards_and_delegated_fields_and_expects_exactly_twelve_cards () :
    deck = butilib.Deck.new()
    
    card_list = deck.pop_some(12)
    cantar_input = butilib.CantarInput(cards=butilib.CardSet(cards=card_list), delegated=False)
    assert isinstance(cantar_input, butilib.CantarInput)
    assert cantar_input.cards.cards == card_list
    assert cantar_input.delegated == False
    
    card_list = deck.pop_some(6)
    pytest.raises(pydantic.ValidationError, butilib.CantarInput, cards=butilib.CardSet(cards=card_list), delegated=True)
    
    card_list = deck.pop_some(14)
    pytest.raises(pydantic.ValidationError, butilib.CantarInput, cards=butilib.CardSet(cards=card_list), delegated=True)
    
def test_cantar_output_is_a_subclass_of_pydantic_base_model () :
    assert issubclass(butilib.CantarOutput, pydantic.BaseModel)
    
def test_cantar_output_has_optional_suit_field_a_butifarra_field_and_delegate_field_that_can_not_be_two_set_to_a_positive_state () :
    cantar_output = butilib.CantarOutput(suit=butilib.OROS)
    assert isinstance(cantar_output, butilib.CantarOutput)
    assert cantar_output.suit == butilib.OROS
    assert cantar_output.delegate == False
    assert cantar_output.butifarra == False
    
    cantar_output = butilib.CantarOutput(delegate=True)
    assert isinstance(cantar_output, butilib.CantarOutput)
    assert cantar_output.suit == None
    assert cantar_output.delegate == True
    assert cantar_output.butifarra == False
    
    cantar_output = butilib.CantarOutput(butifarra=True)
    assert isinstance(cantar_output, butilib.CantarOutput)
    assert cantar_output.suit == None
    assert cantar_output.delegate == False
    assert cantar_output.butifarra == True
    
    pytest.raises(pydantic.ValidationError, butilib.CantarOutput, suit=butilib.OROS, delegate=True, butifarra=True)
    pytest.raises(pydantic.ValidationError, butilib.CantarOutput, suit=butilib.OROS, delegate=True)
    pytest.raises(pydantic.ValidationError, butilib.CantarOutput, suit=butilib.OROS, butifarra=True)
    pytest.raises(pydantic.ValidationError, butilib.CantarOutput, delegate=True, butifarra=True)
    pytest.raises(pydantic.ValidationError, butilib.CantarOutput)
    
def test_contrar_input_is_a_subclass_of_pydantic_base_model () :
    assert issubclass(butilib.ContrarInput, pydantic.BaseModel)

def test_contrar_input_has_full_card_set_player_delegated_triumph_score_contrada_attributes () :
    deck = butilib.Deck.new()
    card_set, _, _, _ = deck.deal()
    
    contrar_input = butilib.ContrarInput(
        cards=card_set,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (12, 0),
        contrada = butilib.NORMAL
    )
    
    assert isinstance(contrar_input, butilib.ContrarInput)
    assert card_set.cards == contrar_input.cards.cards
    assert contrar_input.player == 1
    assert contrar_input.delegated == False
    assert contrar_input.triumph == butilib.OROS
    assert contrar_input.score == (12, 0)
    assert contrar_input.contrada == butilib.NORMAL
    
def test_contrar_input_cards_property_has_exactly_12_cards () :
    deck = butilib.Deck.new()
    
    cards1 = butilib.CardSet(cards=deck.pop_some(10))
    cards2 = butilib.CardSet(cards=deck.pop_some(13))
    
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards1,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (12, 0),
        contrada = butilib.NORMAL
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards2,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (12, 0),
        contrada = butilib.NORMAL
        )
    
def test_contrar_input_player_attribute_can_only_have_values_in_the_range_0_to_3 () :
    deck = butilib.Deck.new()
    cards, _, _, _ = deck.deal()
    
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=-1,
        delegated=False,
        triumph=butilib.OROS,
        score = (12, 0),
        contrada = butilib.NORMAL
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=4,
        delegated=False,
        triumph=butilib.OROS,
        score = (12, 0),
        contrada = butilib.NORMAL
        )
    
def test_cantar_input_score_atribute_holds_two_int_values_between_0_and_101 () :
    deck = butilib.Deck.new()
    cards, _, _, _ = deck.deal()
    
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (-1, 10),
        contrada = butilib.NORMAL
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (30, -30),
        contrada = butilib.NORMAL
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (-12, -4),
        contrada = butilib.NORMAL
        )
    
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (120, 4),
        contrada = butilib.NORMAL
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (1, 400),
        contrada = butilib.NORMAL
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (122, -4),
        contrada = butilib.NORMAL
        )

def test_contrar_input_checks_if_it_is_possible_to_be_in_that_situation () :
    deck = butilib.Deck.new()
    cards, _, _, _ = deck.deal()
    
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=0,
        delegated=False,
        triumph=butilib.OROS,
        score = (1, 10),
        contrada = butilib.NORMAL
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=2,
        delegated=False,
        triumph=butilib.OROS,
        score = (1, 10),
        contrada = butilib.NORMAL
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (1, 10),
        contrada = butilib.CONTRADA
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=3,
        delegated=False,
        triumph=butilib.OROS,
        score = (1, 10),
        contrada = butilib.CONTRADA
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=1,
        delegated=False,
        triumph=butilib.OROS,
        score = (1, 10),
        contrada = butilib.SANT_VICENTADA
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=2,
        delegated=False,
        triumph=butilib.OROS,
        score = (1, 10),
        contrada = butilib.RECONTRADA
        )
    pytest.raises(pydantic.ValidationError, butilib.ContrarInput,
        cards=cards,
        player=0,
        delegated=False,
        triumph=butilib.OROS,
        score = (1, 10),
        contrada = butilib.RECONTRADA
        )
    
def test_contrar_output_is_a_pydantic_base_model () :
    assert issubclass(butilib.ContrarOutput, pydantic.BaseModel)
    
def test_contrar_output_has_contrar_bool_attribute () :
    contrar_output = butilib.ContrarOutput(contrar=False)
    assert isinstance(contrar_output, butilib.ContrarOutput)
    assert contrar_output.contrar == False
    
def test_play_input_is_a_pydantic_base_model () :
    assert issubclass(butilib.PlayInput, pydantic.BaseModel)

def test_play_input_has_history_card_set_triumph_butifarra_player_number_cards_contrada_delegated_player_c () :
    deck = butilib.Deck.new()
    card_set, _, _, _ = deck.deal()
    play_input = butilib.PlayInput(
        history=butilib.History(bazas=[]),
        card_set=card_set, triumph=butilib.OROS,
        player_number=0, cards=[], contrada=butilib.NORMAL,
        delegated=False, player_c=1 
    )
    
    assert isinstance(play_input, butilib.PlayInput)
    assert play_input.history == butilib.History(bazas=[])
    assert play_input.card_set == card_set
    assert play_input.triumph == butilib.OROS
    assert play_input.butifarra == False
    assert play_input.player_number == 0
    assert play_input.cards == []
    assert play_input.contrada == butilib.NORMAL
    assert play_input.player_c == 1
    assert play_input.delegated == False
    
    deck = butilib.Deck.new()
    card_set, _, _, _ = deck.deal()
    play_input = butilib.PlayInput(
        history=butilib.History(bazas=[]),
        card_set=card_set, butifarra=True,
        player_number=0, cards=[], contrada=butilib.NORMAL,
        delegated=False, player_c=1 
    )
    
    assert isinstance(play_input, butilib.PlayInput)
    assert play_input.history == butilib.History(bazas=[])
    assert play_input.card_set == card_set
    assert play_input.triumph == None
    assert play_input.butifarra == True
    assert play_input.player_number == 0
    assert play_input.cards == []
    assert play_input.contrada == butilib.NORMAL
    assert play_input.player_c == 1
    assert play_input.delegated == False
    
def test_play_input_player_number_is_between_0_and_3 () :
    deck = butilib.Deck.new()
    card_set, _, _, _ = deck.deal()
    pytest.raises(pydantic.ValidationError, butilib.PlayInput,
        history=butilib.History(bazas=[]),
        card_set=card_set, butifarra=True,
        player_number=-1, cards=[], contrada=butilib.NORMAL,
        delegated=False, player_c=1 
    )
    pytest.raises(pydantic.ValidationError, butilib.PlayInput,
        history=butilib.History(bazas=[]),
        card_set=card_set, butifarra=True,
        player_number=4, cards=[], contrada=butilib.NORMAL,
        delegated=False, player_c=1
    )
    
def test_play_input_player_c_is_between_0_and_3 () :
    deck = butilib.Deck.new()
    card_set, _, _, _ = deck.deal()
    pytest.raises(pydantic.ValidationError, butilib.PlayInput,
        history=butilib.History(bazas=[]),
        card_set=card_set, butifarra=True,
        player_number=1, cards=[], contrada=butilib.NORMAL,
        delegated=False, player_c=-1
    )
    pytest.raises(pydantic.ValidationError, butilib.PlayInput,
        history=butilib.History(bazas=[]),
        card_set=card_set, butifarra=True,
        player_number=1, cards=[], contrada=butilib.NORMAL,
        delegated=False, player_c=4
    )
    
def test_play_input_has_only_one_of_the_fields_butifarra_or_triumph_as_non_negative_values () :
    deck = butilib.Deck.new()
    card_set, _, _, _ = deck.deal()
    pytest.raises(pydantic.ValidationError, butilib.PlayInput,
        history=butilib.History(bazas=[]),
        card_set=card_set, butifarra=True, triumph= butilib.OROS,
        player_number=1, cards=[], contrada=butilib.NORMAL,
        delegated=False, player_c=1
    )
    pytest.raises(pydantic.ValidationError, butilib.PlayInput,
        history=butilib.History(bazas=[]),
        card_set=card_set,
        player_number=1, cards=[], contrada=butilib.NORMAL,
        delegated=False, player_c=1
    )


def test_play_input_checks_that_the_history_is_consistent_with_the_rules () :
    deck = butilib.Deck.new()
    card_set = butilib.CardSet(cards=deck.pop_some(10))
    
    history = butilib.History(bazas=[
        butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.OROS) for i in [8, 10, 12, 9] ]),
        butilib.Baza(initial_player=3, cards=[ butilib.Card(number=i, suit=butilib.ESPADAS) for i in [9, 2, 3, 5] ]),
    ])
    
    # The player_number and cards are not consistent as player 3 started
    pytest.raises(pydantic.ValidationError, butilib.PlayInput,
                  history=history, card_set=card_set, player_number=1, cards=[],
                  triumph=butilib.OROS,
                  contrada=butilib.NORMAL, delegated=False, player_c=1
                )
    
    # The initial players of the bazas do not correspond to winners
    history = butilib.History(bazas=[
        butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.OROS) for i in [8, 10, 12, 9] ]),
        butilib.Baza(initial_player=2, cards=[ butilib.Card(number=i, suit=butilib.ESPADAS) for i in [9, 2, 3, 5] ]),
    ])
    
    pytest.raises(pydantic.ValidationError, butilib.PlayInput,
                  history=history, card_set=card_set, player_number=2, cards=[],
                  triumph=butilib.OROS,
                  contrada=butilib.NORMAL, delegated=False, player_c=1
                )
    
def test_play_input_checks_that_the_number_of_cards_in_the_card_set_is_consistent_with_the_number_of_bazas_in_history () :
    deck = butilib.Deck.new()
    card_set = butilib.CardSet(cards=deck.pop_some(11))
    
    history = butilib.History(bazas=[
        butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.OROS) for i in [8, 10, 12, 9] ]),
        butilib.Baza(initial_player=3, cards=[ butilib.Card(number=i, suit=butilib.ESPADAS) for i in [9, 2, 3, 5] ]),
    ])
    
    pytest.raises(pydantic.ValidationError, butilib.PlayInput,
                history=history, card_set=card_set, player_number=3, cards=[],
                triumph=butilib.OROS,
                contrada=butilib.NORMAL, delegated=False, player_c=1
            )
    
    deck = butilib.Deck.new()
    card_set = butilib.CardSet(cards=deck.pop_some(9))
    
    history = butilib.History(bazas=[
        butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.OROS) for i in [8, 10, 12, 9] ]),
        butilib.Baza(initial_player=3, cards=[ butilib.Card(number=i, suit=butilib.ESPADAS) for i in [9, 2, 3, 5] ]),
    ])
    
    pytest.raises(pydantic.ValidationError, butilib.PlayInput,
                history=history, card_set=card_set, player_number=3, cards=[],
                triumph=butilib.OROS,
                contrada=butilib.NORMAL, delegated=False, player_c=1
            )
    