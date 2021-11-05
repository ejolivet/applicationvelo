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
