from typing import Union, final
from dataclasses import dataclass


class Command:
    pass


@final
@dataclass(frozen=True)
class AddComponentTypeCommand(Command):
    atelier: str
    type_component: str
    parent_type: Union[str, None] = None


@final
@dataclass(frozen=True)
class AddComponentCommand(Command):
    atelier: str
    component_name: str
    component_type: str
    parent_component: Union[str, None] = None


@final
@dataclass(frozen=True)
class InstallComponentOnTargetCommand(Command):
    atelier: str
    component_name: str
    target_name: str
