from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import ItemCreate, ItemRead, ItemUpdate

router = APIRouter()


@router.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "pantry"}


@router.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)) -> ItemRead:
    return ItemRead.model_validate(crud.create_item(db, payload))


@router.get("/items", response_model=list[ItemRead])
def list_items(
    category: str | None = Query(default=None),
    location: str | None = Query(default=None),
    expiring_within_days: int | None = Query(default=None, ge=0),
    db: Session = Depends(get_db),
) -> list[ItemRead]:
    items = crud.list_items(
        db,
        category=category,
        location=location,
        expiring_within_days=expiring_within_days,
    )
    return [ItemRead.model_validate(i) for i in items]


@router.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ItemRead:
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return ItemRead.model_validate(item)


@router.patch("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)) -> ItemRead:
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return ItemRead.model_validate(crud.update_item(db, item, payload))


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    crud.delete_item(db, item)
