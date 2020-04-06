import logging

from grocery.application.factories.user import UserFactory
from grocery.application.repositories.user import UserRepository
from grocery.application.services import Service
from grocery.domain.models.user import User
from grocery.infrastructure import db


class ListUsersService(Service):
    def execute(self) -> User:
        with db.session() as session:
            return UserRepository(session).get_all_users()
