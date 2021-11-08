from typing import List, Dict, Union
from uuid import uuid1

from allocationvelo.domain import model_component_type, model_component
from . import events


class ComponentTypeNotDefined(Exception):
    pass


class ComponentTypeAlreadayExists(Exception):
    pass


class ComponentTypeforParentDoesNotExists(Exception):
    pass


class Atelier:
    def __init__(
        self,
        identifiant: str,
        component_types: List[model_component_type.ComponentType],
        components: List[model_component_type.ComponentType] = [],
    ):
        self.identifiant = identifiant
        self.component_types: Dict(model_component_type.ComponentTypeID, model_component_type.ComponentType) = {
            component_type.identifiant: component_type for component_type in component_types
        }
        self.components: Dict(str, model_component.Component) = {
            component.component_name: component for component in components
        }
        self.events: List[events.Event] = []

    def has_component_type(self, component_type: str) -> bool:
        return any(
            [type_component.type_component == component_type for type_component in self.component_types.values()]
        )

    def has_component(self, component_name: str) -> bool:
        return component_name in self.components

    def define_new_component_type(self, component_type: str, parent_type: Union[str, None] = None) -> None:
        if self.has_component_type(component_type):
            raise ComponentTypeAlreadayExists(f"Component Type {component_type} is already defined!")
        parent_type_id = None
        if parent_type is not None:
            parent_component = self.get_component_type_by_type_value(parent_type)
            if parent_component is None:
                raise ComponentTypeforParentDoesNotExists(
                    f"Component Type {parent_type} as parent but it is not defined!"
                )
            parent_type_id = parent_component.identifiant
        newtype = model_component_type.ComponentType(
            self.identifiant,
            model_component_type.ComponentTypeID(uuid1().hex),
            component_type,
            parent_type_id=parent_type_id,
        )
        self.component_types[newtype.identifiant] = newtype
        self.events.append(events.ComponentTypeCreated(newtype.type_component))

    def get_component_type_by_type_value(self, type_component: str) -> Union[model_component_type.ComponentType, None]:
        for component_type in self.component_types.values():
            if type_component == component_type.type_component:
                return component_type
        return None

    def define_new_component(self, component_name: str, component_type: str, parent_component=str) -> None:
        if not self.has_component_type(component_type):
            raise ComponentTypeNotDefined(f"Component Type {component_type} is not defined!")
        component_type_id = self.get_component_type_by_type_value(component_type).identifiant
        newcomponent = model_component.Component(
            self.identifiant, model_component.ComponentID(uuid1().hex), component_name, component_type_id, None
        )
        self.components[newcomponent.component_name] = newcomponent

    def install_component_on_target(self, component_name: str, target_name: str) -> None:
        self.components[component_name].parent_component_id = self.components[target_name].identifiant
