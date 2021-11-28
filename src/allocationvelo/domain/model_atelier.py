from typing import List, Dict, Union
from uuid import uuid1

from typing import NewType, Optional
from uuid import UUID

from allocationvelo.domain import model_component_type, model_component
from . import events


class ComponentTypeNotDefined(Exception):
    pass


class ComponentTypeAlreadayExists(Exception):
    pass


class ComponentTypeforParentDoesNotExists(Exception):
    pass


AtelierID = NewType("AtelierID", UUID)


class Atelier:
    def __init__(
        self,
        identifiant: AtelierID,
        component_types: List[model_component_type.ComponentType],
        components: List[model_component_type.ComponentType] = [],
    ):
        self.identifiant = identifiant
        self.component_types: Dict(model_component_type.ComponentTypeName, model_component_type.ComponentType) = {
            component_type.name: component_type for component_type in component_types
        }
        self.components: Dict(model_component.ComponentID, model_component.Component) = {
            component.identifiant: component for component in components
        }
        self.events: List[events.Event] = []

    def has_component_type(self, component_type: model_component_type.ComponentTypeName) -> bool:
        return component_type in self.component_types

    # def has_component(self, component_name: str) -> bool:
    #     return component_name in self.components

    def define_new_component_type(
        self,
        component_type: model_component_type.ComponentTypeName,
        parent_type: Optional[model_component_type.ComponentTypeName] = None,
    ) -> None:
        if self.has_component_type(component_type):
            raise ComponentTypeAlreadayExists(f"Component Type {component_type} is already defined!")

        parent_type_name = None
        if parent_type is not None:
            if not self.has_component_type(parent_type):
                raise ComponentTypeforParentDoesNotExists(
                    f"Component Type {parent_type} as parent but it is not defined!"
                )
            parent_type_name = self.component_types[parent_type].name

        newtype = model_component_type.ComponentType(
            name=component_type,
            parent_type_name=parent_type_name,
        )
        self.component_types[newtype.name] = newtype
        self.events.append(events.ComponentTypeCreated(newtype.name))

    # def get_component_type_by_type_value(self, type_component: str) -> Union[model_component_type.ComponentType, None]:
    #     for component_type in self.component_types.values():
    #         if type_component == component_type.type_component:
    #             return component_type
    #     return None

    def define_new_component(
        self,
        component_name: model_component.ComponentName,
        component_type: model_component_type.ComponentTypeName,
        parent_component: Optional[model_component.ComponentID] = None,
    ) -> None:
        if not self.has_component_type(component_type):
            raise ComponentTypeNotDefined(f"Component Type {component_type} is not defined!")
        newcomponent = model_component.Component(component_name, component_type, parent_component)
        self.components[newcomponent.identifiant] = newcomponent
        self.events.append(events.ComponentCreated(newcomponent.component_name))

    def get_component_id_by_name(self, component_name: model_component.ComponentName):
        for id, component in self.components.items():
            if component.component_name == component_name:
                return id
        return None

    def install_component_on_target(self, component_name: str, target_name: str) -> None:
        id = self.get_component_id_by_name(component_name)
        id_parent = self.get_component_id_by_name(target_name)

        self.components[id].parent_component_id = self.components[id_parent].identifiant
