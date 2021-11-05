from typing import Set, Protocol

from allocationvelo.domain.model_atelier import Atelier


class AbstractRepositoryAtelier(Protocol):
    def add(self, product: Atelier):
        ...

    def get(self, sku) -> Atelier:
        ...


class TrackingRepository:
    seen: Set[Atelier]

    def __init__(self, repo: AbstractRepositoryAtelier):
        self.seen = set()  # type: Set[Atelier]
        self._repo = repo

    def add(self, atelier: Atelier):
        self._repo.add(atelier)
        self.seen.add(atelier)

    def get(self, identifiant: str) -> Atelier:
        atelier = self._repo.get(identifiant)
        if atelier:
            self.seen.add(atelier)
        return atelier


class SqlAlchemyRepositoryAtelier:
    def __init__(self, session):
        self.session = session

    def add(self, atelier: Atelier):
        self.session.add(atelier)

    def get(self, identifiant: str):
        return self.session.query(Atelier).filter_by(identifiant=identifiant).first()

    def list(self):
        return self.session.query(Atelier).all()
