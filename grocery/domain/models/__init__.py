import datetime
import uuid
from uuid import UUID


class Entity:
    def __init__(
        self, uuid: UUID, created_at: datetime.datetime, updated_at: datetime.datetime,
    ):
        self.uuid = uuid
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return _repr(self)

    def __eq__(self, other):
        if not type(self) == type(other):
            return False
        return self.uuid == other.uuid

    def __hash__(self):
        return hash(f"{type(self)}_{self.uuid}")


class AggregateRoot(Entity):
    pass


class ValueObject:
    def __eq__(self, other):
        if not type(self) == type(other):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(f"{type(self)}_{self.__dict__}")

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return _repr(self)


def _repr(obj):
    offset = " " * (len(type(obj).__name__) + 2)

    def to_s(x):
        if isinstance(x, datetime.datetime):
            return x.isoformat()
        return str(x)

    res = f"<{type(obj).__name__} "
    res += f" \n{offset}".join([f"{k}={to_s(v)}" for k, v in obj.__dict__.items()])
    res += ">"
    return res
