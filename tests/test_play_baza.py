import pydantic
import pytest

import butilib
from butilib.testing import TestModel


def test_play_baza_input_is_a_pydantic_base_model():
    assert issubclass(butilib.PlayBazaInput, pydantic.BaseModel)


def test_play_baza_input_class_has_all_expected_atributes():
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
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=0,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
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
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=0,
        triumph=butilib.OROS,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
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


def test_play_baza_input_does_not_accept_players_as_a_list_of_more_or_less_than_4_players():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()
    m5 = butilib.Model()

    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4, m5],
        card_sets=[c1, c2, c3, c4],
        initial_player=0,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3],
        card_sets=[c1, c2, c3, c4],
        initial_player=0,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )


def test_play_baza_input_does_not_accept_card_sets_list_to_be_of_length_different_to_4():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    deck = butilib.Deck.new()
    c5, _, _, _ = deck.deal()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4, c5],
        initial_player=0,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3],
        initial_player=0,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )


def test_play_baza_input_does_not_allow_player_numbers_out_of_0_3_range():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=-1,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=4,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=0,
        butifarra=True,
        player_c=-1,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=0,
        butifarra=True,
        player_c=4,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )


def test_play_baza_input_raises_validation_error_if_not_exactly_one_of_the_butifarra_or_triumph_fields_are_set_to_non_none_values():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=0,
        butifarra=True,
        triumph=butilib.OROS,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=0,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )


def test_play_baza_input_raises_error_if_history_is_not_consistent():
    """THIS EXAMPLE IS FULLY CORRECT (Should not raise any error)

    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    c1 = butilib.CardSet(cards=[ butilib.Card(number=9, suit=butilib.OROS) ])
    c2 = butilib.CardSet(cards=[ butilib.Card(number=1, suit=butilib.OROS) ])
    c3 = butilib.CardSet(cards=[ butilib.Card(number=12, suit=butilib.OROS) ])
    c4 = butilib.CardSet(cards=[ butilib.Card(number=11, suit=butilib.OROS) ])

    delegated = False
    player_c = 0
    butifarra = True

    history = butilib.History(bazas=[
        butilib.Baza(initial_player=1, cards=[ butilib.Card(number=i, suit=butilib.OROS) for i in [2, 3, 4, 5] ]),
        butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.OROS) for i in [6, 7, 8, 10] ]),

        butilib.Baza(initial_player=3, cards=[ butilib.Card(number=i, suit=butilib.BASTOS) for i in [2, 3, 4, 5] ]),
        butilib.Baza(initial_player=2, cards=[ butilib.Card(number=i, suit=butilib.BASTOS) for i in [6, 7, 8, 10] ]),
        butilib.Baza(initial_player=1, cards=[ butilib.Card(number=i, suit=butilib.BASTOS) for i in [11, 12, 1, 9] ]),

        butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.ESPADAS) for i in [2, 3, 4, 5] ]),
        butilib.Baza(initial_player=3, cards=[ butilib.Card(number=i, suit=butilib.ESPADAS) for i in [6, 7, 8, 10] ]),
        butilib.Baza(initial_player=2, cards=[ butilib.Card(number=i, suit=butilib.ESPADAS) for i in [11, 12, 1, 9] ]),

        butilib.Baza(initial_player=1, cards=[ butilib.Card(number=i, suit=butilib.COPAS) for i in [2, 3, 4, 5] ]),
        butilib.Baza(initial_player=0, cards=[ butilib.Card(number=i, suit=butilib.COPAS) for i in [6, 7, 8, 10] ]),
        butilib.Baza(initial_player=3, cards=[ butilib.Card(number=i, suit=butilib.COPAS) for i in [11, 12, 1, 9] ]),
    ])

    pytest.raises(pydantic.ValidationError, butilib.PlayBazaInput,
                  history=history, players=[m1, m2, m3, m4], card_sets=[c1, c2, c3, c4],
                  initial_player=2, butifarra=butifarra, player_c=player_c,
                  delegated=delegated, game_variant=butilib.LIBRE,
                  contrada=butilib.NORMAL
                  )
    """

    # Player_c does not match the initial player of the first baza
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    c1 = butilib.CardSet(cards=[butilib.Card(number=9, suit=butilib.OROS)])
    c2 = butilib.CardSet(cards=[butilib.Card(number=1, suit=butilib.OROS)])
    c3 = butilib.CardSet(cards=[butilib.Card(number=12, suit=butilib.OROS)])
    c4 = butilib.CardSet(cards=[butilib.Card(number=11, suit=butilib.OROS)])

    delegated = False
    player_c = 3
    butifarra = True

    history = butilib.History(
        bazas=[
            butilib.Baza(
                initial_player=1,
                cards=[butilib.Card(number=i, suit=butilib.OROS) for i in [2, 3, 4, 5]],
            ),
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=butilib.OROS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=3,
                cards=[
                    butilib.Card(number=i, suit=butilib.BASTOS) for i in [2, 3, 4, 5]
                ],
            ),
            butilib.Baza(
                initial_player=2,
                cards=[
                    butilib.Card(number=i, suit=butilib.BASTOS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=1,
                cards=[
                    butilib.Card(number=i, suit=butilib.BASTOS) for i in [11, 12, 1, 9]
                ],
            ),
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=butilib.ESPADAS) for i in [2, 3, 4, 5]
                ],
            ),
            butilib.Baza(
                initial_player=3,
                cards=[
                    butilib.Card(number=i, suit=butilib.ESPADAS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=2,
                cards=[
                    butilib.Card(number=i, suit=butilib.ESPADAS) for i in [11, 12, 1, 9]
                ],
            ),
            butilib.Baza(
                initial_player=1,
                cards=[
                    butilib.Card(number=i, suit=butilib.COPAS) for i in [2, 3, 4, 5]
                ],
            ),
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=butilib.COPAS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=3,
                cards=[
                    butilib.Card(number=i, suit=butilib.COPAS) for i in [11, 12, 1, 9]
                ],
            ),
        ]
    )

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=history,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=2,
        butifarra=butifarra,
        player_c=player_c,
        delegated=delegated,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    # The winner of a baza does not start the next one
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    c1 = butilib.CardSet(cards=[butilib.Card(number=9, suit=butilib.OROS)])
    c2 = butilib.CardSet(cards=[butilib.Card(number=1, suit=butilib.OROS)])
    c3 = butilib.CardSet(cards=[butilib.Card(number=12, suit=butilib.OROS)])
    c4 = butilib.CardSet(cards=[butilib.Card(number=11, suit=butilib.OROS)])

    delegated = False
    player_c = 0
    butifarra = True

    history = butilib.History(
        bazas=[
            butilib.Baza(
                initial_player=1,
                cards=[butilib.Card(number=i, suit=butilib.OROS) for i in [2, 3, 4, 5]],
            ),
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=butilib.OROS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=3,
                cards=[
                    butilib.Card(number=i, suit=butilib.BASTOS) for i in [2, 3, 4, 5]
                ],
            ),
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=butilib.BASTOS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=1,
                cards=[
                    butilib.Card(number=i, suit=butilib.BASTOS) for i in [11, 12, 1, 9]
                ],
            ),
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=butilib.ESPADAS) for i in [2, 3, 4, 5]
                ],
            ),
            butilib.Baza(
                initial_player=3,
                cards=[
                    butilib.Card(number=i, suit=butilib.ESPADAS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=2,
                cards=[
                    butilib.Card(number=i, suit=butilib.ESPADAS) for i in [11, 12, 1, 9]
                ],
            ),
            butilib.Baza(
                initial_player=1,
                cards=[
                    butilib.Card(number=i, suit=butilib.COPAS) for i in [2, 3, 4, 5]
                ],
            ),
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=butilib.COPAS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=3,
                cards=[
                    butilib.Card(number=i, suit=butilib.COPAS) for i in [11, 12, 1, 9]
                ],
            ),
        ]
    )

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=history,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=2,
        butifarra=butifarra,
        player_c=player_c,
        delegated=delegated,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    # The winner of the last baza isn't the initial player of the actual baza
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    c1 = butilib.CardSet(cards=[butilib.Card(number=9, suit=butilib.OROS)])
    c2 = butilib.CardSet(cards=[butilib.Card(number=1, suit=butilib.OROS)])
    c3 = butilib.CardSet(cards=[butilib.Card(number=12, suit=butilib.OROS)])
    c4 = butilib.CardSet(cards=[butilib.Card(number=11, suit=butilib.OROS)])

    delegated = False
    player_c = 0
    butifarra = True

    history = butilib.History(
        bazas=[
            butilib.Baza(
                initial_player=1,
                cards=[butilib.Card(number=i, suit=butilib.OROS) for i in [2, 3, 4, 5]],
            ),
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=butilib.OROS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=3,
                cards=[
                    butilib.Card(number=i, suit=butilib.BASTOS) for i in [2, 3, 4, 5]
                ],
            ),
            butilib.Baza(
                initial_player=2,
                cards=[
                    butilib.Card(number=i, suit=butilib.BASTOS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=1,
                cards=[
                    butilib.Card(number=i, suit=butilib.BASTOS) for i in [11, 12, 1, 9]
                ],
            ),
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=butilib.ESPADAS) for i in [2, 3, 4, 5]
                ],
            ),
            butilib.Baza(
                initial_player=3,
                cards=[
                    butilib.Card(number=i, suit=butilib.ESPADAS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=2,
                cards=[
                    butilib.Card(number=i, suit=butilib.ESPADAS) for i in [11, 12, 1, 9]
                ],
            ),
            butilib.Baza(
                initial_player=1,
                cards=[
                    butilib.Card(number=i, suit=butilib.COPAS) for i in [2, 3, 4, 5]
                ],
            ),
            butilib.Baza(
                initial_player=0,
                cards=[
                    butilib.Card(number=i, suit=butilib.COPAS) for i in [6, 7, 8, 10]
                ],
            ),
            butilib.Baza(
                initial_player=3,
                cards=[
                    butilib.Card(number=i, suit=butilib.COPAS) for i in [11, 12, 1, 9]
                ],
            ),
        ]
    )

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=history,
        players=[m1, m2, m3, m4],
        card_sets=[c1, c2, c3, c4],
        initial_player=3,
        butifarra=butifarra,
        player_c=player_c,
        delegated=delegated,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )


def test_play_baza_input_raises_an_error_if_not_all_the_card_sets_are_of_the_same_length():
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    c1.pop()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        card_sets=[c1, c2, c3, c4],
        players=[m1, m2, m3, m4],
        initial_player=0,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )


def test_play_baza_input_raises_an_error_if_the_number_of_cards_in_a_card_set_is_inconsistent_with_the_number_of_bazas_in_history():
    m1 = butilib.Model()
    m2 = butilib.Model()
    m3 = butilib.Model()
    m4 = butilib.Model()

    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(
            bazas=[
                butilib.Baza(
                    initial_player=0,
                    cards=[
                        butilib.Card(number=i, suit=butilib.OROS)
                        for i in [9, 1, 12, 11]
                    ],
                )
            ]
        ),
        card_sets=[c1, c2, c3, c4],
        players=[m1, m2, m3, m4],
        initial_player=0,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    cards = []

    cards.append(c1.pop())
    c1.pop()

    cards.append(c2.pop())
    c2.pop()

    cards.append(c3.pop())
    c3.pop()

    cards.append(c4.pop())
    c4.pop()

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[butilib.Baza(initial_player=0, cards=cards)]),
        card_sets=[c1, c2, c3, c4],
        players=[m1, m2, m3, m4],
        initial_player=0,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )


def test_play_baza_input_raises_an_error_if_there_are_any_repeated_cards_in_any_card_set_or_history():
    # Check for repeated cards in the card sets
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
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[]),
        card_sets=[c1, c2, c3, c4],
        players=[m1, m2, m3, m4],
        initial_player=0,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    # Check for repeated cards including the history
    deck = butilib.Deck.new()
    c1, c2, c3, c4 = deck.deal()

    cards = [c1.pop(), c2.pop(), c3.pop(), c4.pop()]

    c1.pop()
    c1.add(cards[0])

    pytest.raises(
        pydantic.ValidationError,
        butilib.PlayBazaInput,
        history=butilib.History(bazas=[butilib.Baza(initial_player=0, cards=cards)]),
        card_sets=[c1, c2, c3, c4],
        players=[m1, m2, m3, m4],
        initial_player=0,
        butifarra=True,
        player_c=3,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )


def test_play_baza_output_is_a_pydantic_base_model():
    issubclass(butilib.PlayBazaOutput, pydantic.BaseModel)


def test_play_baza_output_has_expected_attributes():
    """PlayBazaOutput:
    - baza: Baza (full baza)
    """
    play_baza_output = butilib.PlayBazaOutput(
        baza=butilib.Baza(
            initial_player=0,
            cards=[butilib.Card(number=i, suit=butilib.OROS) for i in [1, 2, 3, 4]],
        )
    )

    assert isinstance(play_baza_output, butilib.PlayBazaOutput)
    assert play_baza_output.baza == butilib.Baza(
        initial_player=0,
        cards=[butilib.Card(number=i, suit=butilib.OROS) for i in [1, 2, 3, 4]],
    )


def test_play_baza_function_expects_a_play_baza_input_and_returns_the_expected_play_baza_output():
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

    m1 = TestModel(card_list=[butilib.Card(number=1, suit=butilib.OROS)])
    m2 = TestModel(card_list=[butilib.Card(number=1, suit=butilib.BASTOS)])
    m3 = TestModel(card_list=[butilib.Card(number=1, suit=butilib.COPAS)])
    m4 = TestModel(card_list=[butilib.Card(number=1, suit=butilib.ESPADAS)])

    play_baza_input = butilib.PlayBazaInput(
        history=butilib.History(bazas=[]),
        card_sets=[c1, c2, c3, c4],
        players=[m1, m2, m3, m4],
        initial_player=1,
        butifarra=True,
        player_c=0,
        delegated=False,
        game_variant=butilib.LIBRE,
        contrada=butilib.NORMAL,
    )

    output = butilib.play_baza(play_baza_input)

    assert isinstance(output, butilib.PlayBazaOutput)
    assert output.baza == butilib.Baza(
        initial_player=1,
        cards=[
            butilib.Card(number=1, suit=butilib.BASTOS),
            butilib.Card(number=1, suit=butilib.COPAS),
            butilib.Card(number=1, suit=butilib.ESPADAS),
            butilib.Card(number=1, suit=butilib.OROS),
        ],
    )
