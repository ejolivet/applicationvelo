from uuid import uuid1

from allocationvelo.domain.model_component_type import ComponentType, ComponentTypeName


def test_define_type_parent():
    type1 = ComponentType(ComponentTypeName("TYPE1"))
    type2 = ComponentType(ComponentTypeName("TYPE2"))
    type2.sub_component_type_of(type1)

    assert type2.parent_type_id == type1.name
