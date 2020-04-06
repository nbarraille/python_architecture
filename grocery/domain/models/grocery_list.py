import datetime
from typing import List, Optional
from uuid import UUID

from grocery.domain.models import AggregateRoot, ValueObject


class Item(ValueObject):
    def __init__(self, position: int, product: str, quantity: int, is_done: bool):
        super().__init__()
        self.position = position
        self.product = product
        self.quantity = quantity
        self.is_done = is_done


class GroceryList(AggregateRoot):
    def __init__(
        self,
        *,
        name: str = None,
        user_uuid: UUID = None,
        items: List[Item] = None,
        uuid: Optional[UUID] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None,
    ):
        if not items:
            items = []
        super().__init__(uuid, created_at, updated_at)
        self.name = name
        self.user_uuid = user_uuid
        self.items = items

    def remaining_items(self):
        return len([item for item in self.items if not item.is_done])

    def is_finished(self):
        return self.remaining_items() == 0
