from pydantic import BaseModel

from .schema import CantarInput, CantarOutput, ContrarInput, ContrarOutput, PlayInput, PlayOutput

class Model (BaseModel) :
    def cantar (self, input: CantarInput) -> CantarOutput :
        output = self._cantar(input)
        
        if input.delegated and output.delegate :
            raise ValueError("The current implementation of _cantar has returned delegate = True from a delegated call.")
        
        return output
    
    def _cantar (self, input: CantarInput) -> CantarOutput :
        raise NotImplementedError("You should implement _cantar method on a subclass.")
    
    def contrar (self, input: ContrarInput) -> ContrarOutput :
        output = self._contrar(input)
        return output
    
    def _contrar (self, input: ContrarInput) -> ContrarOutput :
        raise NotImplementedError("You should implement _contrar method on a subclass.")
    
    def play (self, input: PlayInput) -> PlayOutput :
        if len(input.cards) != 0 :
            initial_player = (input.player_number - len(input.cards)) % 4
            winning_player = initial_player
            winning_card = input.cards[0]
            f_suit = winning_card.suit
            
            if input.butifarra :
                t1 = f_suit
                t2 = None
            else :
                t1 = input.triumph
                t2 = f_suit
            
            for i in range(1, len(input.cards)) :
                card = input.cards[i] 
                
                if card.compare(winning_card, t1, t2) :
                    winning_player = (initial_player + i) % 4
                    winning_card = card
                    
            desc = input.card_set.describe()
            
            if desc[f_suit].number > 0 :
                if desc[f_suit].number == 1 :
                    card = input.card_set.get(suit=f_suit)[0]
                    return PlayOutput(card=card, forced=True)
                elif (winning_player - input.player_number) % 2 == 1  :
                    cards = [ c for c in input.card_set.get(suit=f_suit) if c.compare(winning_card, t1, t2) ]
                    if len(cards) == 1 :
                        return PlayOutput(card=cards[0], forced=True)
                    elif len(cards) > 1 :
                        p_cards = cards
                    else:
                        p_cards = input.card_set.get(suit=f_suit)
                else :
                    p_cards = input.card_set.get(suit=f_suit)
            else :
                if (winning_player - input.player_number) % 2 == 1 :
                    if input.triumph is not None and desc[input.triumph].number > 0 :
                        cards = [ c for c in input.card_set.get(suit=input.triumph) if c.compare(winning_card, t1, t2) ]
                        if len(cards) == 1 :
                            return PlayOutput(card=cards[0], forced=True)
                        elif len(cards) > 1 :
                            p_cards = cards
                        else :
                            p_cards = input.card_set.cards
                    else :
                        p_cards = input.card_set.cards
                else :
                    p_cards = input.card_set.cards
        else :
            p_cards = input.card_set.cards
        
        output = self._play(input)
        
        if output.card not in p_cards :
            raise ValueError("Returned card is not a valid card")
        
        return output
    
    def _play (self, input: ContrarInput) -> ContrarOutput :
        raise NotImplementedError("You should implement _play method on a subclass.")