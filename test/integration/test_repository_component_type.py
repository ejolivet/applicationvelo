# pylint: disable=protected-access
from allocationvelo.domain import model_component_type
from allocationvelo.adapters import repository_port_component_type


def test_repository_can_save_a_component_type(session):
    compoenent_type = model_component_type.ComponentType(name="Type1", parent_type_name=None)

    repo = repository_port_component_type.SqlAlchemyRepositoryComponentType(session)
    repo.add(compoenent_type)
    session.commit()

    rows = session.execute('SELECT name, parent_type_name FROM "tb_component_types"')
    assert list(rows) == [("Type1", None)]


def test_repository_can_save_a_component_type_with_parent(session):
    compoenent_type = model_component_type.ComponentType(name="Type1", parent_type_name="Type1Parent")

    repo = repository_port_component_type.SqlAlchemyRepositoryComponentType(session)
    repo.add(compoenent_type)
    session.commit()

    rows = session.execute('SELECT name, parent_type_name FROM "tb_component_types"')
    assert list(rows) == [("Type1", "Type1Parent")]
