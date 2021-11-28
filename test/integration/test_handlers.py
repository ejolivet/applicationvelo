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
    message_bus.handle(commands.AddComponentTypeCommand(atelier="atelier", type_component="Type1"), uow)

    message_bus.handle(
        commands.AddComponentTypeCommand(atelier="atelier", type_component="Type2", parent_type="Type1"), uow
    )

    assert (
        uow.ateliers.get("atelier").component_types["Type1"].name
        == uow.ateliers.get("atelier").component_types["Type2"].parent_type_name
    )


def test_can_not_add_new_component_type_with_non_existing_parent(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type1"), uow)

    with pytest.raises(model_atelier.ComponentTypeforParentDoesNotExists, match="Undefined_Type"):
        message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type2", "Undefined_Type"), uow)

    assert len(uow.ateliers.get("atelier").component_types) == 1


def test_can_add_new_component(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type1"), uow)

    message_bus.handle(commands.AddComponentCommand("atelier", "New Component", "Type1"), uow)
    expected_component_identifiant = next(iter(uow.ateliers.get("atelier").components.items()))[0]

    assert expected_component_identifiant in uow.ateliers.get("atelier").components
    assert uow.ateliers.get("atelier").components[expected_component_identifiant].component_name == "New Component"


def test_can_not_add_new_component_with_undefined_type(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type1"), uow)

    with pytest.raises(model_atelier.ComponentTypeNotDefined, match="Undefined_Type"):
        message_bus.handle(commands.AddComponentCommand("atelier", "New Component", "Undefined_Type"), uow)

    assert len(uow.ateliers.get("atelier").components) == 0


def test_can_install_component_on_target_component(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    message_bus.handle(commands.AddComponentTypeCommand("atelier", "Type1"), uow)
    message_bus.handle(commands.AddComponentCommand("atelier", "Component1", "Type1"), uow)
    message_bus.handle(commands.AddComponentCommand("atelier", "Component2", "Type1"), uow)

    message_bus.handle(commands.InstallComponentOnTargetCommand("atelier", "Component2", "Component1"), uow)

    assert uow.ateliers.get("atelier").components[
        uow.ateliers.get("atelier").get_component_id_by_name("Component2")
    ].parent_component_id == uow.ateliers.get("atelier").get_component_id_by_name("Component1")
