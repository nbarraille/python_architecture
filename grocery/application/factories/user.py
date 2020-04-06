import datetime
import uuid

from grocery.application.factories import Factory
from grocery.domain.models.user import User


class UserFactory(Factory):
    @staticmethod
    def create(name: str) -> User:
        return User(
            uuid=uuid.uuid4(),
            name=name,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
