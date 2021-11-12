from typing import Set, Protocol

from allocationvelo.domain.model_component import Component, ComponentID


class AbstractRepositoryComponent(Protocol):
    def add(self, product: Component):
        ...

    def get(self, identifiant: ComponentID) -> Component:
        ...


class TrackingRepository:
    seen: Set[Component]

    def __init__(self, repo: AbstractRepositoryComponent):
        self.seen = set()  # type: Set[Component]
        self._repo = repo

    def add(self, component: Component):
        self._repo.add(component)
        self.seen.add(component)

    def get(self, identifiant: ComponentID) -> Component:
        component = self._repo.get(identifiant)
        if component:
            self.seen.add(component)
        return component


class SqlAlchemyRepositoryComponent:
    def __init__(self, session):
        self.session = session

    def add(self, component_type: Component):
        self.session.add(component_type)

    def get(self, identifiant: ComponentID):
        return self.session.query(Component).filter_by(identifiant=identifiant).first()

    def list(self):
        return self.session.query(Component).all()
