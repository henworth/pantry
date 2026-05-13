from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Item
from app.schemas import ItemCreate, ItemUpdate


def create_item(db: Session, payload: ItemCreate) -> Item:
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, item_id: int) -> Item | None:
    return db.get(Item, item_id)


def list_items(
    db: Session,
    *,
    category: str | None = None,
    location: str | None = None,
    expiring_within_days: int | None = None,
) -> list[Item]:
    stmt = select(Item)
    if category is not None:
        stmt = stmt.where(Item.category == category)
    if location is not None:
        stmt = stmt.where(Item.location == location)
    if expiring_within_days is not None:
        cutoff = date.today() + timedelta(days=expiring_within_days)
        stmt = stmt.where(Item.expiration_date.is_not(None)).where(
            Item.expiration_date <= cutoff
        )
    return list(db.scalars(stmt.order_by(Item.id.desc())))


def update_item(db: Session, item: Item, payload: ItemUpdate) -> Item:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: Item) -> None:
    db.delete(item)
    db.commit()
