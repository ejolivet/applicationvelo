# pylint: disable=protected-access
from allocationvelo.domain import model_component
from allocationvelo.adapters import repository_port_component


def test_repository_can_save_a_component(session):
    compoenent = model_component.Component(
        component_name=model_component.ComponentName("Component1"),
        component_type=model_component.ComponentTypeName("Type1"),
    )

    repo = repository_port_component.SqlAlchemyRepositoryComponent(session)
    repo.add(compoenent)
    session.commit()

    rows = session.execute('SELECT component_name, component_type, parent_component_id FROM "tb_components"')
    assert list(rows) == [("Component1", "Type1", None)]


def test_repository_can_save_a_component_with_parent(session):
    compoenent = model_component.Component(
        component_name=model_component.ComponentName("Component1"),
        component_type=model_component.ComponentTypeName("Type1"),
        parent_component_id=model_component.ComponentID("200"),
    )
    repo = repository_port_component.SqlAlchemyRepositoryComponent(session)
    repo.add(compoenent)
    session.commit()

    rows = session.execute('SELECT component_name, component_type, parent_component_id FROM "tb_components"')
    assert list(rows) == [("Component1", "Type1", "200")]
