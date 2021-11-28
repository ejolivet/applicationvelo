from typing import Set, Protocol

from allocationvelo.domain.model_atelier import Atelier, AtelierID


class AbstractRepositoryAtelier(Protocol):
    def add(self, component_type: Atelier):
        ...

    def get(self, atelierid: AtelierID) -> Atelier:
        ...


class TrackingRepository:
    seen: Set[Atelier]

    def __init__(self, repo: AbstractRepositoryAtelier):
        self.seen = set()  # type: Set[Atelier]
        self._repo = repo

    def add(self, atelier: Atelier):
        self._repo.add(atelier)
        self.seen.add(atelier)

    def get(self, aterlierid: AtelierID) -> Atelier:
        atelier = self._repo.get(aterlierid)
        if atelier:
            self.seen.add(atelier)
        return atelier


class SqlAlchemyRepositoryAtelier:
    def __init__(self, session):
        self.session = session

    def add(self, atelier: Atelier):
        self.session.add(atelier)

    def get(self, atelierid: AtelierID) -> Atelier:
        return self.session.query(Atelier).filter_by(identifiant=atelierid).first()

    def list(self):
        return self.session.query(Atelier).all()
