from fastapi import APIRouter, HTTPException
import httpx
from pymongo import MongoClient
import redis

router = APIRouter()

# MongoDB Connection
try:
    mongo_client = MongoClient("mongodb://localhost:27017/")
    db = mongo_client["mydatabase"]
except Exception as e:
    raise Exception(f"MongoDB Connection Error: {str(e)}")

# Redis Connection
try:
    cache = redis.Redis(host="localhost", port=6379, decode_responses=True)
except Exception as e:
    raise Exception(f"Redis Connection Error: {str(e)}")


# API-1: Fetch data from MongoDB
@router.get("/mongo-data")
def get_mongo_data():
    try:
        data = list(db["collection"].find({}, {"_id": 0}))
        return {"mongo_data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB Fetch Error: {str(e)}")


# API-2: Fetch data from Cache
@router.get("/cache-data")
def get_cache_data():
    try:
        data = cache.get("cached_key")
        if data is None:
            raise HTTPException(status_code=404, detail="Cache key not found")
        return {"cache_data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache Fetch Error: {str(e)}")


# API-3: Fetch data from both MongoDB and Cache
@router.get("/mongo-cache-data")
def get_mongo_cache_data():
    try:
        mongo_data = list(db["collection"].find({}, {"_id": 0}))
        cache_data = cache.get("cached_key")
        if cache_data is None:
            cache_data = "No cache data found"
        return {"mongo_data": mongo_data, "cache_data": cache_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB/Cache Fetch Error: {str(e)}")


# API-4: Fetch data from an external API
@router.get("/external-api")
async def get_external_api():
    try:
        async with httpx.AsyncClient(timeout=5) as client:  # 5-second timeout
            # response = await client.get("https://fakestoreapi.com/products/1")
            # response.raise_for_status()  # Raises an error for non-200 responses
            return "I am External API Response"
    except httpx.HTTPStatusError as http_err:
        raise HTTPException(status_code=500, detail=f"External API Error: {str(http_err)}")
    except httpx.RequestError as req_err:
        raise HTTPException(status_code=500, detail=f"External API Request Failed: {str(req_err)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")
