# app/database.py

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch MongoDB URI and Database Name from environment variables
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "vodex_db")

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)

# Access the specified database
db = client[DATABASE_NAME]

# Define collections
items_collection = db.get_collection("items")
clock_in_collection = db.get_collection("clock_in_records")
