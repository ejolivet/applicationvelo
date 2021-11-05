# pylint: disable=attribute-defined-outside-init
from __future__ import annotations
import abc
from sqlalchemy.orm.session import Session

from allocationvelo.adapters import repository_port


class AbstractUnitOfWorkAtelier(abc.ABC):
    ateliers: repository_port.AbstractRepositoryAtelier

    def __enter__(self) -> AbstractUnitOfWorkAtelier:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    def collect_new_events(self):
        for atelier in self.ateliers.seen:
            while atelier.events:
                yield atelier.events.pop(0)


class SqlAlchemyUnitOfWorkAtelier(AbstractUnitOfWorkAtelier):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.ateliers = repository_port.TrackingRepository(repository_port.SqlAlchemyRepositoryAtelier(self.session))
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
