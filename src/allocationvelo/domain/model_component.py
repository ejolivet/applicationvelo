from __future__ import annotations
from typing import NewType, Union
from uuid import UUID

from .model_component_type import ComponentTypeID

ComponentID = NewType("ComponentID", UUID)


class Component:
    def __init__(
        self,
        atelier: str,
        identifiant: ComponentID,
        component_name: str,
        type_component: ComponentTypeID,
        parent_component_id: Union[None, ComponentID] = None,
    ):
        self.atelier = atelier
        self.identifiant: ComponentID = identifiant
        self.component_name: str = component_name
        self.type_component: ComponentTypeID = type_component
        self.parent_component_id: Union[ComponentID, None] = parent_component_id

    # def __repr__(self) -> str:
    #     return self.type_component

    def __hash__(self):
        return hash(self.identifiant)

    def __eq__(self, other):
        if not isinstance(other, Component):
            return False
        return other.type_component == self.type_component

    def sub_component_of(self, component: Component) -> None:
        self.parent_component_id = component.identifiant
