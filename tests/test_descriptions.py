import pydantic
import pytest
import butilib

def test_suit_description_is_a_pydantic_base_model () :
    assert issubclass(butilib.SuitDescription, pydantic.BaseModel)
    
def test_suit_description_has_number_and_points_atributes () :
    suit_description = butilib.SuitDescription(number=8, points=4)
    assert suit_description.number == 8
    assert suit_description.points == 4

def test_card_set_description_inherits_from_pydantic_base_model () :
    assert issubclass(butilib.CardSetDescription, pydantic.BaseModel)
    
def test_card_set_description_has_four_attributes_one_for_each_field_of_type_suit_description () :
    cs_desc = butilib.CardSetDescription(
        oros = butilib.SuitDescription(number=1, points=1),
        bastos = butilib.SuitDescription(number=1, points=1),
        espadas = butilib.SuitDescription(number=1, points=1),
        copas = butilib.SuitDescription(number=1, points=1),
    )
    
    assert isinstance(cs_desc.oros, butilib.SuitDescription)
    assert isinstance(cs_desc.bastos, butilib.SuitDescription)
    assert isinstance(cs_desc.copas, butilib.SuitDescription)
    assert isinstance(cs_desc.espadas, butilib.SuitDescription)
    
    assert cs_desc.oros == butilib.SuitDescription(number=1, points=1)
    assert cs_desc.bastos == butilib.SuitDescription(number=1, points=1)
    assert cs_desc.copas == butilib.SuitDescription(number=1, points=1)
    assert cs_desc.espadas == butilib.SuitDescription(number=1, points=1)
    
def test_card_set_description_attributes_can_be_accessed_as_a_dict () :
    cs_desc = butilib.CardSetDescription(
        oros = butilib.SuitDescription(number=1, points=1),
        bastos = butilib.SuitDescription(number=1, points=1),
        espadas = butilib.SuitDescription(number=1, points=1),
        copas = butilib.SuitDescription(number=1, points=1),
    )
    
    for s in butilib.Suit :
        assert cs_desc[s] == butilib.SuitDescription(number=1, points=1)
        
    with pytest.raises(KeyError) :
        cs_desc["Invalid Key"]
        
def test_card_set_description_attributes_can_be_set_as_a_dict () :
    cs_desc = butilib.CardSetDescription(
        oros = butilib.SuitDescription(number=1, points=1),
        bastos = butilib.SuitDescription(number=1, points=1),
        espadas = butilib.SuitDescription(number=1, points=1),
        copas = butilib.SuitDescription(number=1, points=1),
    )
    
    i = 5
    for s in butilib.Suit :
        cs_desc[s] = butilib.SuitDescription(number=i, points=3)
        assert cs_desc[s] == butilib.SuitDescription(number=i, points=3)
        i += 1 
    
    with pytest.raises(KeyError) :
        cs_desc["Invalid Key"] == butilib.SuitDescription(number=0, points=3)