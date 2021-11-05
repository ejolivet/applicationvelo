from __future__ import annotations
from typing import NewType, Union, Dict, Set, List
from uuid import UUID

from dataclasses import dataclass

from .model_component_type import ComponentType

# class UnAuthorizedComponent(Exception):
#     pass


# class ComponentTypeAllReadyInstalled(Exception):
#     pass


# class ComponentAllReadyInstalled(Exception):
#     pass


# class ComponentUnInstalled(Exception):
#     pass


ComponentID = NewType("ComponentID", UUID)
ComponentTypeID = NewType("ComponentTypeID", UUID)


def install_component(target: Component, component: Component):
    target.install_component(component)


def remove_component(target: Component, component: Component):
    target.remove_component(component)


@dataclass(unsafe_hash=True)
class ComponentDTO:
    identifiant: ComponentID
    component_type_id: ComponentTypeID
    components_list_id: Union[List[ComponentID], None] = None
    component_type_list_id: Union[List[ComponentTypeID], None] = None
    install_on_id: Union[ComponentID, None] = None


class Component:
    def __init__(
        self,
        identifiant: ComponentID,
        component_type: ComponentType,
        list_authorized_components: Union[None, Set[ComponentType]] = None,
    ):
        self.identifiant: ComponentID = identifiant
        if list_authorized_components is None:
            list_authorized_components = set()
        self.__component_type: ComponentType = component_type
        self.__components: Dict[ComponentTypeID, Union[ComponentID, None]] = {
            comp.identifiant: None for comp in list_authorized_components
        }
        self.__installed_on: Union[ComponentID, None] = None

    def __eq__(self, other):
        if not isinstance(other, Component):
            return False
        return other.identifiant == self.identifiant

    def __hash__(self):
        return hash(self.identifiant)

    @property
    def component_type(self) -> ComponentType:
        return self.__component_type

    @property
    def install_status(self) -> Union[ComponentID, None]:
        return self.__installed_on

    @install_status.setter
    def install_status(self, install_status: Union[ComponentID, None]):
        self.__installed_on = install_status

    def to_component_dto(self):
        return ComponentDTO(
            identifiant=self.identifiant.hex,
            component_type_id=self.component_type.identifiant.hex,
            component_type_list_id=[componenttypeid.hex for componenttypeid in self.__components],
            install_on_id=self.__installed_on.hex if self.__installed_on is not None else None,
            components_list_id=[
                component.identifiant.hex if component is not None else None for component in self.__components.values()
            ],
        )

    def is_authorized_component(self, component: Component):
        return component.component_type in self.__components

    # def can_install(self, component: Component):
    #     if not self.is_authorized_component(component):
    #         raise UnAuthorizedComponent(f"Component {component.component_type} is not authorized")
    #     if self.is_component_installed(component):
    #         raise ComponentAllReadyInstalled(
    #             f"Component {component.component_type}-{component.identifiant} is allready installed"
    #         )
    #     if self.is_type_installed(component.component_type):
    #         raise ComponentTypeAllReadyInstalled(f"Component {component.component_type} is allready installed")
    #     return True

    # def install_component(self, component: Component) -> None:
    #     if self.can_install(component):
    #         component.install_status = self.identifiant
    #         self.__components[component.component_type.identifiant] = component.identifiant

    # def is_component_installed(self, component: Component) -> bool:
    #     if not self.is_type_installed(component.component_type):
    #         return False
    #     return self.__components[component.component_type.identifiant] == component.identifiant

    # def is_type_installed(self, component_type_check: ComponentType) -> bool:
    #     if component_type_check not in self.__components:
    #         return False
    #     return self.__components[component_type_check.identifiant] is not None

    # def remove_component(self, component: Component) -> None:
    #     if self.is_component_installed(component):
    #         self.__components[component.component_type.identifiant] = None
    #         component.install_status = None
    #     else:
    #         raise ComponentUnInstalled(
    #             f"Component {component.component_type}-{component.identifiant} is allready installed"
    #         )
