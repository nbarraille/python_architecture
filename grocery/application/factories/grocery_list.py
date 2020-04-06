import datetime
import uuid

from grocery.application.factories import Factory
from grocery.domain.models.grocery_list import GroceryList
from grocery.domain.models.user import User


class GroceryListFactory(Factory):
    @staticmethod
    def create(name: str, user: User) -> GroceryList:
        return GroceryList(
            uuid=uuid.uuid4(),
            name=name,
            user_uuid=user.uuid,
            items=[],
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
