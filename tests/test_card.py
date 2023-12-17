import pydantic

import butilib

def test_card_object_is_a_pydantic_base_model ():
    assert issubclass(butilib.Card, pydantic.BaseModel)