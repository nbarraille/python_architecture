import datetime
import uuid

from grocery.domain.models.user import User


class TestUser:
    def test_user_same_uuid(self):
        my_uuid = uuid.uuid4()
        user1 = User(
            name="Nathan",
            uuid=my_uuid,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        user2 = User(
            name="Nate",
            uuid=my_uuid,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        assert user1 == user2
