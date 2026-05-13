from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str | None = Field(default=None, max_length=60)
    quantity: float = Field(default=1.0, ge=0)
    unit: str = Field(default="pcs", max_length=20)
    expiration_date: date | None = None
    location: str | None = Field(default=None, max_length=40)
    notes: str | None = Field(default=None, max_length=500)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    category: str | None = Field(default=None, max_length=60)
    quantity: float | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, max_length=20)
    expiration_date: date | None = None
    location: str | None = Field(default=None, max_length=40)
    notes: str | None = Field(default=None, max_length=500)


class ItemRead(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
