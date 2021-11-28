from typing import Set, Protocol

from allocationvelo.domain.model_component_type import ComponentType, ComponentTypeName


class AbstractRepositoryComponentType(Protocol):
    def add(self, component_type: ComponentType):
        ...

    def get(self, typename: ComponentTypeName) -> ComponentType:
        ...


class TrackingRepository:
    seen: Set[ComponentType]

    def __init__(self, repo: AbstractRepositoryComponentType):
        self.seen = set()  # type: Set[ComponentType]
        self._repo = repo

    def add(self, component_type: ComponentType):
        self._repo.add(component_type)
        self.seen.add(component_type)

    def get(self, typename: ComponentTypeName) -> ComponentType:
        component_type = self._repo.get(typename)
        if component_type:
            self.seen.add(component_type)
        return component_type


class SqlAlchemyRepositoryComponentType:
    def __init__(self, session):
        self.session = session

    def add(self, component_type: ComponentType):
        self.session.add(component_type)

    def get(self, typename: ComponentTypeName) -> ComponentType:
        return self.session.query(ComponentType).filter_by(typename=typename).first()

    def list(self):
        return self.session.query(ComponentType).all()
