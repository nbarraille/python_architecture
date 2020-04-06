from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from grocery.application.repositories import Dto, Repository
from grocery.domain.models.grocery_list import GroceryList, Item
from grocery.domain.models.user import User
from grocery.infrastructure.db import Base


class GroceryListRepository(Repository):
    class ItemDto(Base):
        __tablename__ = "grocery_list_items"

        position = Column(Integer, primary_key=True)
        grocery_list_uuid = Column(
            UUID(as_uuid=True), ForeignKey("grocery_lists.uuid"), primary_key=True
        )
        product = Column(String, nullable=False)
        quantity = Column(Integer, nullable=False)
        is_done = Column(Boolean, nullable=False)

        def to_model(self) -> Item:
            return Item(
                position=position,
                product=self.product,
                quantity=self.quantity,
                is_done=self.is_done,
            )

        def from_model(
            cls, item: Item, grocery_list: GroceryListRepository.GroceryListDto
        ) -> ItemDto:
            return ItemDto(
                position=item.position,
                grocery_list_uuid=grocery_list.uuid,
                product=product,
                quantity=quantity,
                is_done=is_done,
            )

    class GroceryListDto(Dto, Base):
        __tablename__ = "grocery_lists"

        # Those can be extracted in base Dto class as they are in base Entity
        uuid = Column(UUID(as_uuid=True), primary_key=True)
        created_at = Column(DateTime, nullable=False)
        updated_at = Column(DateTime, nullable=False)

        # We can probably do some python magic in base Dto to not have to maintain this class
        user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
        name = Column(String, nullable=False)

        # Here we have multiple solutions for persisting a Value Object that is part of an aggregate
        # If it's a 1-1 relationship we can inline it in the model with one column for each attribute
        # If it's a 1 to Many relationship like here with the items, we can inline it with SQL JSON/ARRAY:
        # We can also create a table for it and have a SQL one to many relationship.
        # How we persist it is just an implementation detail of the repository
        # Here I chose to use a SQL table with relationship to keep SQL migration capability\
        # when the ValueObject structure changes

        # items = Column(JSONB, nullable=False)
        items = relationship(
            "ItemDto", lazy="selectin"
        )  # Important: We want lazy loading here

        def to_model(self) -> GroceryList:
            items = [item_dto.to_model() for item_dto in self.items]
            return GroceryList(
                uuid=self.uuid,
                user_uuid=self.user_uuid,
                created_at=self.created_at,
                updated_at=self.updated_at,
                name=self.name,
                items=items,
            )

        @classmethod
        def from_model(
            cls, grocery_list: GroceryList
        ) -> GroceryListRepository.GroceryListDto:
            list_dto = GroceryListRepository.GroceryListDto(
                uuid=grocery_list.uuid,
                created_at=grocery_list.created_at,
                updated_at=grocery_list.updated_at,
                name=grocery_list.name,
                user_uuid=grocery_list.user_uuid,
            )
            list_dto.items = [
                GroceryListRepository.ItemDto.from_model(item, list_dto)
                for item in grocery_list.items
            ]
            return list_dto

    def get_lists_for_user(self, user: User) -> List[GroceryList]:
        dtos = (
            self.session.query(GroceryListRepository.GroceryListDto)
            .filter_by(user_uuid=user.uuid)
            .all()
        )
        return [dto.to_model() for dto in dtos]

    def get_list_by_id(self, uuid: UUID) -> GroceryList:
        return (
            self.session.query(GroceryListRepository.GroceryListDto)
            .filter_by(uuid=uuid)
            .first()
            .to_model()
        )

    def save(self, grocery_list: GroceryList) -> None:
        self.session.save(GroceryListRepository.GroceryListDto.from_model(grocery_list))
