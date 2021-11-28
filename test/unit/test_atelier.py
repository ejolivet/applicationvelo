from uuid import uuid1
import pytest

from allocationvelo.domain.model_component_type import ComponentType, ComponentTypeName
from allocationvelo.domain.model_atelier import (
    Atelier,
    ComponentTypeAlreadayExists,
    ComponentTypeforParentDoesNotExists,
    ComponentTypeNotDefined,
)


def test_can_define_new_component_type():
    type1 = ComponentType(ComponentTypeName("Type1"))
    type2 = ComponentType(ComponentTypeName("Type2"))
    atelier = Atelier(ComponentTypeName("atelier"), [type1, type2])
    atelier.define_new_component_type(component_type="Type3")
    assert len(atelier.component_types) == 3


def test_can_not_define_same_component_type_twice():
    type1 = ComponentType(ComponentTypeName("Type1"))
    type2 = ComponentType(ComponentTypeName("Type2"))
    atelier = Atelier(ComponentTypeName("atelier"), [type1, type2])
    with pytest.raises(ComponentTypeAlreadayExists, match="Type2"):
        atelier.define_new_component_type(component_type="Type2")
    assert len(atelier.component_types) == 2


def test_can_define_new_component_type_with_parent():
    type1 = ComponentType(ComponentTypeName("Type1"))
    type2 = ComponentType(ComponentTypeName("Type2"))
    atelier = Atelier(ComponentTypeName("atelier"), [type1, type2])
    atelier.define_new_component_type(component_type="Type3", parent_type=type1.parent_type_name)
    assert len(atelier.component_types) == 3


def test_cant_define_new_component_type_with_unexisted_parent():
    type1 = ComponentType(ComponentTypeName("Type1"))
    type2 = ComponentType(ComponentTypeName("Type2"))
    atelier = Atelier(ComponentTypeName("atelier"), [type1, type2])

    with pytest.raises(ComponentTypeforParentDoesNotExists, match="Type_undefined"):
        atelier.define_new_component_type(component_type="Type3", parent_type="Type_undefined")

    assert len(atelier.component_types) == 2


def test_can_define_new_component_with_existing_component_type():
    type1 = ComponentType(ComponentTypeName("Type1"))
    atelier = Atelier(ComponentTypeName("atelier"), [type1])

    atelier.define_new_component(component_name="Component1", component_type="Type1")

    assert len(atelier.component_types) == 1


def test_can_not_define_new_component_with_unexisting_component_type():
    type1 = ComponentType(ComponentTypeName("Type1"))
    atelier = Atelier(ComponentTypeName("atelier"), [type1])

    with pytest.raises(ComponentTypeNotDefined, match="Typeundefined"):
        atelier.define_new_component(component_name="Component1", component_type="Typeundefined")

    assert len(atelier.component_types) == 1
