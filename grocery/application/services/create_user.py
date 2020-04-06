import logging

from grocery.application.factories.user import UserFactory
from grocery.application.repositories.user import UserRepository
from grocery.application.services import Service
from grocery.domain.models.user import User
from grocery.infrastructure import db
from grocery.infrastructure.db import ResourceConflictError


class CreateUserService(Service):
    def __init__(self, user_name: str):
        super().__init__()
        self.user_name = user_name

    def execute(self) -> User:
        try:
            with db.session() as session:
                user = UserFactory.create(name=self.user_name)
                repo = UserRepository(session)
                repo.save(user)
            logging.info(f"User successfully created {user}")
            return user
        except ResourceConflictError as e:
            logging.error(f"User with name {name} already exists", exc_info=True)
