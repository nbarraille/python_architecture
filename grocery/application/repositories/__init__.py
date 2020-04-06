from __future__ import annotations

from grocery.domain.models import AggregateRoot
from grocery.infrastructure.db import DbSession


class Repository:
    def __init__(self, session: DbSession):
        self.session = session


class Dto:
    def to_model(self) -> AggregateRoot:
        raise NotImplementedError()

    @classmethod
    def from_model(cls, model: AggregateRoot) -> Dto:
        raise NotImplementedError()
