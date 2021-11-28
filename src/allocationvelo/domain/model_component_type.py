from __future__ import annotations
from typing import NewType, Optional
from uuid import UUID

ComponentTypeName = NewType("ComponentTypeName", str)


class ComponentType:
    def __init__(
        self,
        name: ComponentTypeName,
        parent_type_name: Optional[ComponentTypeName] = None,
    ):
        self.name: ComponentTypeName = name
        self.parent_type_name: Optional[ComponentTypeName] = parent_type_name

    # def __repr__(self) -> str:
    #     return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, ComponentType):
            return False
        return other.name == self.name

    def sub_component_type_of(self, component_type: ComponentType) -> None:
        self.parent_type_name = component_type.name
