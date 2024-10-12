# app/routers/items.py

from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, date

from app.schemas import Item, ItemCreate, ItemUpdate
from app.database import items_collection
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

# ---------- Create a New Item ----------
@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    item = jsonable_encoder(item)
    item["insert_date"] = datetime.utcnow()
    new_item = await items_collection.insert_one(item)
    created_item = await items_collection.find_one({"_id": new_item.inserted_id})
    return created_item

# ---------- Retrieve an Item by ID ----------
@router.get("/{id}", response_model=Item)
async def get_item(id: str = Path(..., title="The ID of the item to retrieve")):
    if (item := await items_collection.find_one({"_id": ObjectId(id)})) is not None:
        return item
    raise HTTPException(status_code=404, detail="Item not found")

# ---------- Filter Items ----------
@router.get("/filter", response_model=List[Item])
async def filter_items(
    email: Optional[str] = Query(None, description="Filter by exact email"),
    expiry_date: Optional[date] = Query(None, description="Filter items expiring after this date (YYYY-MM-DD)"),
    insert_date: Optional[datetime] = Query(None, description="Filter items inserted after this datetime (YYYY-MM-DDTHH:MM:SS)"),
    quantity: Optional[int] = Query(None, ge=1, description="Filter items with quantity >= this value")
):
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gt": expiry_date}
    if insert_date:
        query["insert_date"] = {"$gt": insert_date}
    if quantity:
        query["quantity"] = {"$gte": quantity}
    
    items = []
    async for item in items_collection.find(query):
        items.append(item)
    return items

# ---------- MongoDB Aggregation: Count Items per Email ----------
@router.get("/aggregate", response_model=List[dict])
async def aggregate_items():
    pipeline = [
        {"$group": {"_id": "$email", "count": {"$sum": 1}}}
    ]
    aggregation = []
    async for doc in items_collection.aggregate(pipeline):
        aggregation.append({"email": doc["_id"], "count": doc["count"]})
    return aggregation

# ---------- Delete an Item by ID ----------
@router.delete("/{id}", response_model=dict)
async def delete_item(id: str = Path(..., title="The ID of the item to delete")):
    delete_result = await items_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

# ---------- Update an Item by ID ----------
@router.put("/{id}", response_model=Item)
async def update_item(id: str, item: ItemUpdate):
    item = {k: v for k, v in item.dict().items() if v is not None}
    if item:
        update_result = await items_collection.update_one({"_id": ObjectId(id)}, {"$set": item})
        if update_result.modified_count == 1:
            if (updated_item := await items_collection.find_one({"_id": ObjectId(id)})) is not None:
                return updated_item
    if (existing_item := await items_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_item
    raise HTTPException(status_code=404, detail="Item not found")
