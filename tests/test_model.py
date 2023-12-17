import pytest
import pydantic

import butilib

def test_model_class_inherits_from_pydantic_base_model () :
    assert issubclass(butilib.Model, pydantic.BaseModel)
    
