from pydantic import BaseModel, conlist

from .card import Card


class CantarInput (BaseModel) :
    cards: conlist(Card, max_length=12, min_length=12)
    delegated: bool