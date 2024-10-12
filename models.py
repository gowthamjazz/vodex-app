# app/models.py

from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import Optional, List
from datetime import datetime

from .schemas import Item, ItemCreate, ItemUpdate, ClockInRecord, ClockInCreate, ClockInUpdate
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class ItemModel:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_item(self, item: ItemCreate) -> Item:
        item_dict = jsonable_encoder(item)
        item_dict["insert_date"] = datetime.utcnow()
        new_item = await self.collection.insert_one(item_dict)
        created_item = await self.collection.find_one({"_id": new_item.inserted_id})
        return Item(**created_item)

    async def get_item(self, id: str) -> Optional[Item]:
        item = await self.collection.find_one({"_id": ObjectId(id)})
        if item:
            return Item(**item)
        return None

    async def update_item(self, id: str, item: ItemUpdate) -> Optional[Item]:
        item_data = {k: v for k, v in item.dict().items() if v is not None}
        if item_data:
            await self.collection.update_one({"_id": ObjectId(id)}, {"$set": item_data})
            updated_item = await self.collection.find_one({"_id": ObjectId(id)})
            if updated_item:
                return Item(**updated_item)
        return None

    async def delete_item(self, id: str) -> bool:
        delete_result = await self.collection.delete_one({"_id": ObjectId(id)})
        return delete_result.deleted_count == 1

    async def filter_items(self, query: dict) -> List[Item]:
        cursor = self.collection.find(query)
        items = []
        async for document in cursor:
            items.append(Item(**document))
        return items

    async def aggregate_items(self) -> List[dict]:
        pipeline = [
            {"$group": {"_id": "$email", "count": {"$sum": 1}}}
        ]
        aggregation = []
        async for doc in self.collection.aggregate(pipeline):
            aggregation.append({"email": doc["_id"], "count": doc["count"]})
        return aggregation

class ClockInModel:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_clock_in(self, record: ClockInCreate) -> ClockInRecord:
        record_dict = jsonable_encoder(record)
        record_dict["insert_datetime"] = datetime.utcnow()
        new_record = await self.collection.insert_one(record_dict)
        created_record = await self.collection.find_one({"_id": new_record.inserted_id})
        return ClockInRecord(**created_record)

    async def get_clock_in(self, id: str) -> Optional[ClockInRecord]:
        record = await self.collection.find_one({"_id": ObjectId(id)})
        if record:
            return ClockInRecord(**record)
        return None

    async def update_clock_in(self, id: str, record: ClockInUpdate) -> Optional[ClockInRecord]:
        record_data = {k: v for k, v in record.dict().items() if v is not None}
        if record_data:
            await self.collection.update_one({"_id": ObjectId(id)}, {"$set": record_data})
            updated_record = await self.collection.find_one({"_id": ObjectId(id)})
            if updated_record:
                return ClockInRecord(**updated_record)
        return None

    async def delete_clock_in(self, id: str) -> bool:
        delete_result = await self.collection.delete_one({"_id": ObjectId(id)})
        return delete_result.deleted_count == 1

    async def filter_clock_in_records(self, query: dict) -> List[ClockInRecord]:
        cursor = self.collection.find(query)
        records = []
        async for document in cursor:
            records.append(ClockInRecord(**document))
        return records
