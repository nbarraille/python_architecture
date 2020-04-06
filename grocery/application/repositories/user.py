from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from grocery.application.repositories import Dto, Repository
from grocery.domain.models.user import User
from grocery.infrastructure.db import Base


class UserRepository(Repository):
    class UserDto(Dto, Base):
        __tablename__ = "users"

        # Those can be extracted in base Dto class as they are in base Entity
        uuid = Column(UUID(as_uuid=True), primary_key=True)
        created_at = Column(DateTime, nullable=False)
        updated_at = Column(DateTime, nullable=False)

        # We can probably do some python magic in base Dto to not have to maintain this class
        name = Column(String, nullable=False, unique=True)

        def to_model(self) -> User:
            return User(
                uuid=self.uuid,
                created_at=self.created_at,
                updated_at=self.updated_at,
                name=self.name,
            )

        @classmethod
        def from_model(self, user: User) -> UserRepository.UserDto:
            return UserRepository.UserDto(
                uuid=user.uuid,
                created_at=user.created_at,
                updated_at=user.updated_at,
                name=user.name,
            )

    def get_user_by_id(self, uuid: UUID) -> User:
        return (
            self.session.query(UserRepository.UserDto)
            .filter_by(uuid=uuid)
            .first()
            .to_model()
        )

    def get_user_by_name(self, name: str) -> User:
        return (
            self.session.query(UserRepository.UserDto)
            .filter_by(name=name)
            .first()
            .to_model()
        )

    def get_all_users(self) -> List[User]:
        dtos = self.session.query(UserRepository.UserDto).all()
        return [dto.to_model() for dto in dtos]

    def save(self, user: User) -> None:
        self.session.save(UserRepository.UserDto.from_model(user))
