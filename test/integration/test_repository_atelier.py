# pylint: disable=protected-access
from allocationvelo.domain import model_atelier, model_component_type, model_component
from allocationvelo.adapters import repository_port_atelier


def test_repository_can_save_a_atelier(session):
    atelier = model_atelier.Atelier(model_atelier.AtelierID("atelier"), component_types=[])

    repo = repository_port_atelier.SqlAlchemyRepositoryAtelier(session)
    repo.add(atelier)
    session.commit()

    rows = session.execute('SELECT identifiant FROM "tb_ateliers"')
    assert list(rows) == [("atelier",)]


def test_repository_can_save_a_atelier_with_a_component_type(session):
    atelier = model_atelier.Atelier(model_atelier.AtelierID("atelier"), component_types=[])
    atelier.define_new_component_type(component_type="Type1", parent_type=None)

    repo = repository_port_atelier.SqlAlchemyRepositoryAtelier(session)
    repo.add(atelier)
    session.commit()

    rows = session.execute('SELECT identifiant FROM "tb_ateliers"')
    assert list(rows) == [("atelier",)]
    rows2 = session.execute('SELECT * FROM "tb_allocation_component_types"')
    assert list(rows2) == [(1, "atelier", "Type1")]


def test_repository_can_retrieve_a_atelier_with_a_component_type(session):
    session.execute('INSERT INTO "tb_component_types" (name, parent_type_name) VALUES ("Type1", "None")')
    session.execute('INSERT INTO "tb_component_types" (name, parent_type_name) VALUES ("Type2", "Type1")')
    session.execute('INSERT INTO "tb_ateliers" (identifiant) VALUES ("atelier1")')
    session.execute(
        'INSERT INTO "tb_allocation_component_types" (atelier_identifiant, component_type_name) VALUES ("atelier1","Type1")'
    )
    session.execute(
        'INSERT INTO "tb_allocation_component_types" (atelier_identifiant, component_type_name) VALUES ("atelier1","Type2")'
    )

    repo = repository_port_atelier.SqlAlchemyRepositoryAtelier(session)
    atelier = repo.get("atelier1")

    expected_component_type1 = model_component_type.ComponentType(model_component_type.ComponentTypeName("Type1"))
    expected_component_type2 = model_component_type.ComponentType(
        model_component_type.ComponentTypeName("Type2"), parent_type_name="Type1"
    )

    assert len(atelier.component_types) == 2
    assert expected_component_type1.name in atelier.component_types
    assert atelier.component_types[expected_component_type1.name] == expected_component_type1
    assert expected_component_type2.name in atelier.component_types
    assert atelier.component_types[expected_component_type2.name] == expected_component_type2


def test_repository_can_save_a_atelier_with_a_component(session):
    atelier = model_atelier.Atelier(model_atelier.AtelierID("atelier"), component_types=[])
    atelier.define_new_component_type(component_type="Type1", parent_type=None)
    atelier.define_new_component(component_name="component1", component_type="Type1")
    expected_component_identifiant = next(iter(atelier.components.items()))[0]

    repo = repository_port_atelier.SqlAlchemyRepositoryAtelier(session)
    repo.add(atelier)
    session.commit()

    rows = session.execute('SELECT identifiant FROM "tb_ateliers"')
    assert list(rows) == [("atelier",)]
    rows2 = session.execute('SELECT * FROM "tb_allocation_components"')
    assert list(rows2) == [(1, "atelier", f"{expected_component_identifiant}")]


def test_repository_can_retrieve_a_atelier_with_a_component(session):
    session.execute('INSERT INTO "tb_component_types" (name, parent_type_name) VALUES ("Type1", "None")')
    session.execute('INSERT INTO "tb_component_types" (name, parent_type_name) VALUES ("Type2", "Type1")')
    session.execute('INSERT INTO "tb_ateliers" (identifiant) VALUES ("atelier1")')
    session.execute(
        'INSERT INTO "tb_allocation_component_types" (atelier_identifiant, component_type_name) VALUES ("atelier1","Type1")'
    )
    session.execute(
        'INSERT INTO "tb_allocation_component_types" (atelier_identifiant, component_type_name) VALUES ("atelier1","Type2")'
    )
    component_id = model_component.ComponentID("id_test")
    session.execute(
        'INSERT INTO "tb_components" (identifiant, component_name, component_type, parent_component_id) VALUES ("id_test", "Component1", "Type1", "None")'
    )
    session.execute(
        'INSERT INTO "tb_allocation_components" (atelier_identifiant, component_identifiant) VALUES ("atelier1","id_test")'
    )

    repo = repository_port_atelier.SqlAlchemyRepositoryAtelier(session)
    atelier = repo.get("atelier1")

    assert len(atelier.component_types) == 2
    assert len(atelier.components) == 1
    assert "id_test" in atelier.components
    assert atelier.components["id_test"].component_name == "Component1"
    assert atelier.components["id_test"].component_type == "Type1"
