import pytest

from allocationvelo.domain import commands, model_atelier
from allocationvelo.services import unit_of_work
from allocationvelo.services import message_bus


def test_can_add_new_component_type(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type1"), uow)
    assert uow.ateliers.get("atelier").has_component_type("Type1") == True


def test_can_not_add_new_component_type_already_defined(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type1"), uow)
    message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type2"), uow)
    with pytest.raises(model_atelier.ComponentTypeAlreadayExists, match="Type2"):
        message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type2"), uow)
    assert len(uow.ateliers.get("atelier").component_types) == 2


def test_can_add_new_component_type_with_existing_parent(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type1"), uow)
    message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type2", "Type1"), uow)
    assert (
        uow.ateliers.get("atelier").get_component_type_by_type_value("Type1").identifiant
        == uow.ateliers.get("atelier").get_component_type_by_type_value("Type2").parent_type_id
    )


def test_can_not_add_new_component_type_with_non_existing_parent(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type1"), uow)
    with pytest.raises(model_atelier.ComponentTypeforParentDoesNotExists, match="Type_unexisting"):
        message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type2", "Type_unexisting"), uow)
    assert len(uow.ateliers.get("atelier").component_types) == 1
