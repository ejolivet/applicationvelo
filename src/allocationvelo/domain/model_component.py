from __future__ import annotations
from typing import NewType, Union
from uuid import UUID, uuid1

from .model_component_type import ComponentTypeName

ComponentID = NewType("ComponentID", str)
ComponentName = NewType("ComponentName", str)


class Component:
    def __init__(
        self,
        component_name: ComponentName,
        component_type: ComponentTypeName,
        parent_component_id: Union[None, ComponentID] = None,
    ):
        self.identifiant: ComponentID = ComponentID(uuid1().hex)
        self.component_name: ComponentName = component_name
        self.component_type: ComponentTypeName = component_type
        self.parent_component_id: Union[ComponentID, None] = parent_component_id

    # def __repr__(self) -> str:
    #     return self.component_type

    def __hash__(self):
        return hash(self.identifiant)

    def __eq__(self, other):
        if not isinstance(other, Component):
            return False
        return other.component_type == self.component_type

    def sub_component_of(self, component: Component) -> None:
        self.parent_component_id = component.identifiant
