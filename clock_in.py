# app/routers/clock_in.py

from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.schemas import ClockInRecord, ClockInCreate, ClockInUpdate
from app.database import clock_in_collection
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/clock-in",
    tags=["Clock-In Records"]
)

# ---------- Create a New Clock-In Record ----------
@router.post("/", response_model=ClockInRecord, status_code=201)
async def create_clock_in(record: ClockInCreate):
    record = jsonable_encoder(record)
    record["insert_datetime"] = datetime.utcnow()
    new_record = await clock_in_collection.insert_one(record)
    created_record = await clock_in_collection.find_one({"_id": new_record.inserted_id})
    return created_record

# ---------- Retrieve a Clock-In Record by ID ----------
@router.get("/{id}", response_model=ClockInRecord)
async def get_clock_in(id: str = Path(..., title="The ID of the clock-in record to retrieve")):
    if (record := await clock_in_collection.find_one({"_id": ObjectId(id)})) is not None:
        return record
    raise HTTPException(status_code=404, detail="Clock-in record not found")

# ---------- Filter Clock-In Records ----------
@router.get("/filter", response_model=List[ClockInRecord])
async def filter_clock_in_records(
    email: Optional[str] = Query(None, description="Filter by exact email"),
    location: Optional[str] = Query(None, description="Filter by exact location"),
    insert_datetime: Optional[datetime] = Query(None, description="Filter clock-ins after this datetime (YYYY-MM-DDTHH:MM:SS)")
):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_datetime:
        query["insert_datetime"] = {"$gt": insert_datetime}
    
    records = []
    async for record in clock_in_collection.find(query):
        records.append(record)
    return records

# ---------- Delete a Clock-In Record by ID ----------
@router.delete("/{id}", response_model=dict)
async def delete_clock_in(id: str = Path(..., title="The ID of the clock-in record to delete")):
    delete_result = await clock_in_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Clock-in record deleted successfully"}
    raise HTTPException(status_code=404, detail="Clock-in record not found")

# ---------- Update a Clock-In Record by ID ----------
@router.put("/{id}", response_model=ClockInRecord)
async def update_clock_in(id: str, record: ClockInUpdate):
    record = {k: v for k, v in record.dict().items() if v is not None}
    if record:
        update_result = await clock_in_collection.update_one({"_id": ObjectId(id)}, {"$set": record})
        if update_result.modified_count == 1:
            if (updated_record := await clock_in_collection.find_one({"_id": ObjectId(id)})) is not None:
                return updated_record
    if (existing_record := await clock_in_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_record
    raise HTTPException(status_code=404, detail="Clock-in record not found")
