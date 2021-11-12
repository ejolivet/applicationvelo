from uuid import uuid1

from allocationvelo.domain.model_component import Component, ComponentID, ComponentName
from allocationvelo.domain.model_component_type import ComponentTypeName


def test_define_component_without_parent():
    component = Component(ComponentID("100"), ComponentName("Component1"), ComponentTypeName("Type1"))

    assert component.component_name == "Component1"
    assert component.component_type == "Type1"
    assert component.parent_component_id == None


def test_define_component_with_parent():
    component = Component(
        ComponentID("100"),
        ComponentName("Component1"),
        ComponentTypeName("Type1"),
        parent_component_id=ComponentID("200"),
    )

    assert component.component_name == "Component1"
    assert component.component_type == "Type1"
    assert component.parent_component_id == "200"
