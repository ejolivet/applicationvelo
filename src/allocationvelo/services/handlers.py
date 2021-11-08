from allocationvelo.services import unit_of_work
from allocationvelo.domain import commands
from allocationvelo.domain.model_atelier import Atelier


class AddComponentTypeHandler:
    def __init__(self, uow: unit_of_work.SqlAlchemyUnitOfWorkAtelier):
        self.uow = uow

    def __call__(self, cmd: commands.AddComponentTypeCommand):
        with self.uow:
            atelier: Atelier = self.uow.ateliers.get(cmd.atelier)
            if atelier is None:
                atelier = Atelier(cmd.atelier, component_types=[])
                self.uow.ateliers.add(atelier)
            atelier.define_new_component_type(component_type=cmd.type_component, parent_type=cmd.parent_type)
            self.uow.commit()


class AddComponentHandler:
    def __init__(self, uow: unit_of_work.SqlAlchemyUnitOfWorkAtelier):
        self.uow = uow

    def __call__(self, cmd: commands.AddComponentCommand):
        with self.uow:
            atelier: Atelier = self.uow.ateliers.get(cmd.atelier)
            if atelier is None:
                atelier = Atelier(cmd.atelier, component_types=[])
                self.uow.ateliers.add(atelier)
            atelier.define_new_component(
                component_name=cmd.component_name,
                component_type=cmd.component_type,
                parent_component=cmd.parent_component,
            )
            self.uow.commit()


class InstallComponentOnTargetHandler:
    def __init__(self, uow: unit_of_work.SqlAlchemyUnitOfWorkAtelier):
        self.uow = uow

    def __call__(self, cmd: commands.InstallComponentOnTargetCommand):
        with self.uow:
            atelier: Atelier = self.uow.ateliers.get(cmd.atelier)
            if atelier is None:
                atelier = Atelier(cmd.atelier, component_types=[])
                self.uow.ateliers.add(atelier)
            atelier.install_component_on_target(
                component_name=cmd.component_name,
                target_name=cmd.target_name,
            )
            self.uow.commit()


class NotifyComponentTypeCreatedHandler:
    def __init__(self, uow: unit_of_work.SqlAlchemyUnitOfWorkAtelier):
        self.uow = uow

    def __call__(self, component_type: str):
        print("COMPONENET TYPE CREATED: component_type")


# def notify_component_type_created(component_type: str):
#     print("COMPONENET TYPE CREATED: component_type")
