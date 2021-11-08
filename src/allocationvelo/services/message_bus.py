# pylint: disable=broad-except
from __future__ import annotations
import logging
from typing import List, Dict, Callable, Type, Union, TYPE_CHECKING
from allocationvelo.domain import commands, events
from . import handlers

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


def handle(
    message: Message,
    uow: unit_of_work.AbstractUnitOfWorkAtelier,
):
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, events.Event):
            handle_event(message, queue, uow)
        elif isinstance(message, commands.Command):
            cmd_result = handle_command(message, queue, uow)
            results.append(cmd_result)
        else:
            raise Exception(f"{message} was not an Event or Command")
    return results


def handle_event(
    event: events.Event,
    queue: List[Message],
    uow: unit_of_work.AbstractUnitOfWork,  # pylint: disable=no-member
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug("handling event %s with handler %s", event, handler)
            handler_uow = handler(uow)
            handler_uow(event)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling event %s", event)
            continue


def handle_command(
    command: commands.Command,
    queue: List[Message],
    uow: unit_of_work.AbstractUnitOfWork,  # pylint: disable=no-member
):
    logger.debug("handling command %s", command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        handler_uow = handler(uow)
        result = handler_uow(command)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logger.exception("Exception handling command %s", command)
        raise


EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.ComponentTypeCreated: [handlers.NotifyComponentTypeCreatedHandler],
}

COMMAND_HANDLERS = {
    commands.AddComponentTypeCommand: handlers.AddComponentTypeHandler,
    commands.AddComponentCommand: handlers.AddComponentHandler,
    commands.InstallComponentOnTargetCommand: handlers.InstallComponentOnTargetHandler,
}  # type: Dict[Type[commands.Command], Callable]
