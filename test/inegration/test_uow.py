import pytest

from allocationvelo.domain.model_component_type import ComponentTypeID
from allocationvelo.services import unit_of_work


def create_atelier(session, atelier_name: str):
    session.execute(
        "INSERT INTO tb_ateliers (identifiant) VALUES (:identifiant)",
        dict(identifiant=atelier_name),
    )


def insert_component_type(
    session, atelier: str, identifiant: ComponentTypeID, type_component: str, parent_type_id: ComponentTypeID
):

    session.execute(
        "INSERT INTO tb_component_types (atelier, identifiant, type_component, parent_type_id) "
        " VALUES (:atelier, :identifiant, :type_component, :parent_type_id)",
        dict(atelier=atelier, identifiant=identifiant, type_component=type_component, parent_type_id=parent_type_id),
    )


def get_component_type_parent_id(session, identifiant: ComponentTypeID):
    [[parent_type_id]] = session.execute(
        "SELECT parent_type_id FROM tb_component_types WHERE identifiant=:identifiant",
        dict(identifiant=identifiant),
    )
    return parent_type_id


def test_uow_component_type_can_retrieve_a_component_type_and_define_parent_type_id(session_factory):
    session = session_factory()
    create_atelier(session, "perso")
    insert_component_type(session, "perso", "100", "Type1", None)
    insert_component_type(session, "perso", "200", "Type2", None)
    session.commit()
    expected_parent_id = "100"

    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    with uow:
        atelier = uow.ateliers.get("perso")
        type1 = atelier.get_component_type_by_type_value("Type1")
        type2 = atelier.get_component_type_by_type_value("Type2")
        type2.sub_component_type_of(type1)
        uow.commit()

    parent_identifiant = get_component_type_parent_id(session, "200")

    assert expected_parent_id == parent_identifiant


def test_rolls_back_uncommitted_work_by_default(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    with uow:
        insert_component_type(uow.session, "perso", "100", "Type1", None)

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "tb_component_types"'))
    assert rows == []


def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass

    uow = unit_of_work.SqlAlchemyUnitOfWorkAtelier(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_component_type(uow.session, "perso", "100", "Type1", None)
            raise MyException()

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "tb_component_types"'))
    assert rows == []
