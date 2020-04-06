import datetime
from typing import Optional
from uuid import UUID

from grocery.domain.models import AggregateRoot


class User(AggregateRoot):
    def __init__(
        self,
        *,
        name: str = None,
        uuid: UUID = None,
        created_at: datetime.datetime = None,
        updated_at: datetime.datetime = None,
    ):
        super().__init__(uuid, created_at, updated_at)
        self.name = name

    # Business logic about user goes here
