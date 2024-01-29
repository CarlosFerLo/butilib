from typing import List

from pydantic import BaseModel

from .schema import (
    CantarInput,
    CantarOutput,
    ContrarInput,
    ContrarOutput,
    PlayInput,
    PlayOutput,
)
from .variants import LIBRE, OBLIGADA, GameVariant


class Model(BaseModel):
    """Base Model class of butilib. All deployable models must inherit from this class and implement all desired methods.
    Do not overwrite cantar, contrar or play methods, instead modify the _cantar, _contrar, _play, _play_libre and _play_obligada methods.

    Class Attributes:
        game_types (List[GameType]): The supported game types for this model. Defaults to [ butilib.LIBRE, butilib.OBLIGADA ]
    """

    game_variants: List[GameVariant] = [LIBRE, OBLIGADA]

    def cantar(self, input: CantarInput) -> CantarOutput:
        """The function called when the model has to select a triumph suit.
            Do not overwrite this method, change the _cantar method instead as this method runs extra checks on the input and output.

        Args:
            input (CantarInput): The input of the cantar function

        Raises:
            ValueError: If the _cantar functions tries to delegate a delegated call.

        Returns:
            CantarOutput: The cantar output.
        """
        output = self._cantar(input)

        if input.delegated and output.delegate:
            raise ValueError(
                "The current implementation of _cantar has returned delegate = True from a delegated call."
            )

        return output

    def _cantar(self, input: CantarInput) -> CantarOutput:
        """The function you must overwrite to change how the cantar function does.

        Args:
            input (CantarInput): The input of the cantar function

        Raises:
            NotImplementedError: This raises if ypu did not implement the _cantar method in a subclass of butilib.Model

        Returns:
            CantarOutput: The output of the cantar function.
        """
        raise NotImplementedError("You should implement _cantar method on a subclass.")

    def contrar(self, input: ContrarInput) -> ContrarOutput:
        """The function called when the model has to decide weather or not to contrar.
            Do not overwrite this method, change the _contrar method instead as this method runs extra checks on the input and output.

        Args:
            input (ContrarInput): The input of the contrar function

        Returns:
            ContrarOutput: The cantar output.
        """
        output = self._contrar(input)
        return output

    def _contrar(self, input: ContrarInput) -> ContrarOutput:
        """The function you must overwrite to change how the contrar function does.

        Args:
            input (ContrarInput): The input of the contrar function

        Raises:
            NotImplementedError: This raises if you did not implement the _contrar method in a subclass of butilib.Model

        Returns:
            ContrarOutput: The output of the contrar function.
        """
        raise NotImplementedError("You should implement _contrar method on a subclass.")

    def play(self, input: PlayInput) -> PlayOutput:
        """The function thet gets called when the model has to decide which card to play.
            Do not overwrite this method, change the _play method instead as this method runs extra checks on the input and output.

        Args:
            input (PlayInput): The input of the play function

        Raises:
            ValueError: If the model does not support this game type.

        Returns:
            PlayOutput: Output of the play function.
        """

        if input.game_variant not in self.game_variants:
            raise ValueError(f"This model does not support {input.game_variant}.")

        if len(input.card_set) == 1:
            return PlayOutput(card=input.card_set.cards[0], forced=True)

        if len(input.cards) > 0:
            f_suit = input.cards[0].suit
            desc = input.card_set.describe()

            if desc[f_suit].number == 1:
                card = input.card_set.get(suit=f_suit)[0]
                return PlayOutput(card=card, forced=True)

            initial_player = input.initial_player()
            win_i = 0
            win_card = input.cards[0]

            if input.butifarra is True:
                t1 = f_suit
                t2 = None
            else:
                t1 = input.triumph
                t2 = f_suit

            for i in range(1, len(input.cards)):
                if input.cards[i].compare(win_card, t1, t2):
                    win_i = i
                    win_card = input.cards[i]

            if desc[f_suit].number > 1:
                p_cards = input.card_set.get(suit=f_suit)
                if (initial_player + win_i - input.player_number) % 2 != 0:
                    w_cards = [c for c in p_cards if c.compare(win_card, t1, t2)]

                    if len(w_cards) == 1:
                        return PlayOutput(card=w_cards[0], forced=True)
                    elif len(w_cards) == 0:
                        if input.game_variant is OBLIGADA:
                            lower = None
                            for c in p_cards:
                                if lower is None:
                                    lower = c
                                elif lower.compare(c, t1, t2):
                                    lower = c

                            return PlayOutput(card=lower, forced=True)
                    elif len(w_cards) > 1:
                        p_cards = w_cards

            elif (initial_player + win_i - input.player_number) % 2 != 0:
                if input.butifarra is False:
                    if desc[input.triumph].number == 1:
                        card = input.card_set.get(suit=input.triumph)[0]
                        return PlayOutput(card=card, forced=True)
                    elif desc[input.triumph].number > 1:
                        p_cards = input.card_set.get(suit=input.triumph)
                        w_cards = [c for c in p_cards if c.compare(win_card, t1, t2)]

                        if len(w_cards) == 1:
                            return PlayOutput(card=w_cards[0], forced=True)
                        elif len(w_cards) > 1:
                            p_cards = w_cards
                else:
                    p_cards = input.card_set.cards
            else:
                p_cards = input.card_set.cards
        else:
            p_cards = input.card_set.cards

        if input.game_variant == LIBRE:
            try:
                output = self._play_libre(input)
            except NotImplementedError:
                output = self._play(input)
        else:  # OBLIGADA
            try:
                output = self._play_obligada(input)
            except NotImplementedError:
                output = self._play(input)

        if output.card not in p_cards:
            raise ValueError(
                f"Invalid card {output.card}, returned by the inner play implementation."
            )

        return output

    def _play(self, input: PlayInput) -> PlayOutput:
        """Default function that gets called when play function is called and no specific play method available.

        Args:
            input (PlayInput): The input to the play function.

        Raises:
            NotImplementedError: This raises if you did not implement this method.

        Returns:
            PlayOutput: The output of the play function.
        """
        raise NotImplementedError("You should implement _play method on a subclass.")

    def _play_libre(self, input: PlayInput) -> PlayOutput:
        """Default function that gets called when play function is called with input.game_type==butilib.LIBRE.

        Args:
            input (PlayInput): The input to the play function.

        Raises:
            NotImplementedError: This raises if you did not implement this method.

        Returns:
            PlayOutput: The output of the play function.
        """
        raise NotImplementedError(
            "You should implement _play_libre method on a subclass."
        )

    def _play_obligada(self, input: PlayInput) -> PlayOutput:
        """Default function that gets called when play function is called with input.game_type==butilib.OBLIGADA.

        Args:
            input (PlayInput): The input to the play function.

        Raises:
            NotImplementedError: This raises if you did not implement this method.

        Returns:
            PlayOutput: The output of the play function.
        """
        raise NotImplementedError(
            "You should implement _play_obligada method on a subclass."
        )
