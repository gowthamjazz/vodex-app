# app/schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from bson import ObjectId

# Custom ObjectId validation
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Pydantic configuration for handling ObjectId
class Config:
    json_encoders = {ObjectId: str}
    arbitrary_types_allowed = True

# ---------- Items Schemas ----------

class ItemBase(BaseModel):
    name: str = Field(..., example="gowdham prasath")
    email: EmailStr = Field(..., example="gowdham.prasath@example.com")
    item_name: str = Field(..., example="Laptop")
    quantity: int = Field(..., ge=1, example=10)
    expiry_date: date = Field(..., example="2024-10-12")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, example="gowdham prasath")
    email: Optional[EmailStr] = Field(None, example="gowdham.prasath@example.com")
    item_name: Optional[str] = Field(None, example="Laptop")
    quantity: Optional[int] = Field(None, ge=1, example=10)
    expiry_date: Optional[date] = Field(None, example="2024-10-12")

class Item(ItemBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    insert_date: datetime = Field(default_factory=datetime.utcnow)

    class Config(Config):
        allow_population_by_field_name = True

# ---------- Clock-In Records Schemas ----------

class ClockInBase(BaseModel):
    email: EmailStr = Field(..., example="gowdham.prasath@example.com")
    location: str = Field(..., example="Chennai")

class ClockInCreate(ClockInBase):
    pass

class ClockInUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="gowdham.prasath@example.com")
    location: Optional[str] = Field(None, example="Chennai")

class ClockInRecord(ClockInBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    insert_datetime: datetime = Field(default_factory=datetime.utcnow)

    class Config(Config):
        allow_population_by_field_name = True
