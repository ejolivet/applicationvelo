from __future__ import annotations
from typing import NewType, Union
from uuid import UUID

ComponentTypeID = NewType("ComponentTypeID", UUID)


class ComponentType:
    def __init__(
        self,
        atelier: str,
        identifiant: ComponentTypeID,
        type_component: str,
        parent_type_id: Union[None, ComponentTypeID] = None,
    ):
        self.atelier = atelier
        self.identifiant: ComponentTypeID = identifiant
        self.type_component: str = type_component
        self.parent_type_id: Union[ComponentTypeID, None] = parent_type_id

    # def __repr__(self) -> str:
    #     return self.type_component

    def __hash__(self):
        return hash(self.identifiant)

    def __eq__(self, other):
        if not isinstance(other, ComponentType):
            return False
        return other.type_component == self.type_component

    def sub_component_type_of(self, component_type: ComponentType) -> None:
        self.parent_type_id = component_type.identifiant
