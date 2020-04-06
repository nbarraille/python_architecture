from typing import Dict, List

from grocery.domain.models.user import User


def serialize_users(users: List[User]) -> List:
    return [serialize_user(user) for user in users]


def serialize_user(user: User) -> Dict:
    return {
        "uuid": str(user.uuid),
        "name": user.name,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.created_at.isoformat(),
    }
