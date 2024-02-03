import pydantic
import pytest

import butilib
from butilib.testing import TestModel


def test_play_hand_input_is_a_pydantic_base_model():
    assert issubclass(butilib.PlayHandInput, pydantic.BaseModel)


def test_play_hand_input_has_all_expected_attributes():
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
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4], score=(12, 3), player_c=0
    )

    assert isinstance(play_hand_input, butilib.PlayHandInput)
    assert play_hand_input.players == [m1, m2, m3, m4]
    assert play_hand_input.card_sets == [c1, c2, c3, c4]
    assert play_hand_input.score == (12, 3)
    assert play_hand_input.player_c == 0


def test_play_hand_input_players_has_fixed_length_of_4_elements():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    m5 = butilib.Model()

    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3],
        card_sets=[c1, c2, c3, c4],
        score=(12, 3),
        player_c=0,
    )
    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4, m5],
        card_sets=[c1, c2, c3, c4],
        score=(12, 3),
        player_c=0,
    )


def test_play_hand_input_card_sets_has_fixed_length_of_four_elements():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3],
        score=(12, 3),
        player_c=0,
    )
    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4, c1],
        score=(12, 3),
        player_c=0,
    )


def test_play_hand_input_score_is_a_valid_score():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        score=(-1, 1),
        player_c=0,
    )
    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        score=(1, -1),
        player_c=0,
    )
    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        score=(102, 1),
        player_c=0,
    )
    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        score=(1, 102),
        player_c=0,
    )


def test_play_hand_input_player_c_is_a_number_between_0_and_3():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        score=(1, 1),
        player_c=-1,
    )
    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        score=(1, 1),
        player_c=4,
    )


def test_play_hand_input_all_card_sets_have_exactly_12_cards():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    card = c1.pop()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        score=(1, 1),
        player_c=0,
    )
    c1.add(card)
    c2.add(card)

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        score=(1, 1),
        player_c=0,
    )


def test_play_hand_input_there_are_no_repeated_cards_on_all_the_card_sets():
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

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayHandInput,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        score=(1, 1),
        player_c=0,
    )


def test_play_hand_output_is_a_pydantic_base_model():
    assert issubclass(butilib.PlayHandOutput, pydantic.BaseModel)


def test_play_hand_output_has_all_expected_attributes():
    """PlayHandOutput:
    - history: History (full)
    """
    history = butilib.History(bazas=[])
    for s in butilib.Suit:
        for l in [[9, 1, 12, 11], [10, 8, 7, 6], [5, 4, 3, 2]]:
            history.add(
                butilib.Baza(
                    initial_player=0, cards=[butilib.Card(suit=s, number=n) for n in l]
                )
            )

    play_hand_output = butilib.PlayHandOutput(history=history)

    assert isinstance(play_hand_output, butilib.PlayHandOutput)
    assert play_hand_output.history == history


def test_play_hand_output_accepts_only_full_history():
    history = butilib.History(bazas=[])

    pytest.raises(pydantic.ValidationError, butilib.PlayHandOutput, history=history)

    # Add 11 more bazas iteratively and check that the history is not accepted
    for s in butilib.Suit:
        for l in [[9, 1, 12, 11], [10, 8, 7, 6], [5, 4, 3, 2]]:
            history.add(
                butilib.Baza(
                    initial_player=0, cards=[butilib.Card(suit=s, number=n) for n in l]
                )
            )
            if len(history) < 12:
                pytest.raises(
                    pydantic.ValidationError, butilib.PlayHandOutput, history=history
                )


def test_play_hand_function_expects_play_hand_input_calls_expected_butilib_functions_and_gets_the_expected_play_hand_output():
    c1 = butilib.CardSet(
        cards=[butilib.Card(number=i, suit=butilib.OROS) for i in range(1, 13)]
    )
    c2 = butilib.CardSet(
        cards=[butilib.Card(number=i, suit=butilib.BASTOS) for i in range(1, 13)]
    )
    c3 = butilib.CardSet(
        cards=[butilib.Card(number=i, suit=butilib.COPAS) for i in range(1, 13)]
    )
    c4 = butilib.CardSet(
        cards=[butilib.Card(number=i, suit=butilib.ESPADAS) for i in range(1, 13)]
    )

    m1 = TestModel(card_list=c1.cards, triumph=butilib.OROS)
    m2 = TestModel(card_list=c2.cards)
    m3 = TestModel(card_list=c3.cards)
    m4 = TestModel(card_list=c4.cards)

    play_hand_input = butilib.PlayHandInput(
        players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4], score=(1, 10), player_c=0
    )

    output = butilib.play_hand(play_hand_input)

    expected_history = butilib.History(bazas=[])

    for i in range(1, 13):
        expected_history.add(
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=s)
                    for s in [
                        butilib.OROS,
                        butilib.BASTOS,
                        butilib.COPAS,
                        butilib.ESPADAS,
                    ]
                ],
            )
        )

    assert output.history == expected_history
