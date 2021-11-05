from uuid import uuid1

from allocationvelo.domain.model_component_type import ComponentType, ComponentTypeID


def test_define_type_parent():
    type1 = ComponentType("atelier", ComponentTypeID(uuid1().hex), "TYPE1")
    type2 = ComponentType("atelier", ComponentTypeID(uuid1().hex), "TYPE2")
    type2.sub_component_type_of(type1)

    assert type2.parent_type_id == type1.identifiant
