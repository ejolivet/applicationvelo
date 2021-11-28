# pylint: disable=too-few-public-methods
from typing import final
from dataclasses import dataclass


class Event:
    pass


@final
@dataclass(frozen=True)
class ComponentTypeCreated(Event):
    type: str


@final
@dataclass(frozen=True)
class ComponentCreated(Event):
    component: str
