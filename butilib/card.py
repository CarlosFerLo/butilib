from pydantic import BaseModel, conint

from .schema import Suit

class Card (BaseModel) :
    number: conint(ge=1, le=12)
    suit: Suit