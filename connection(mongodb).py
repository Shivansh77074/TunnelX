"""
Database connection module
"""
# import redis
from pymongo import MongoClient
from config import Config

def get_mongo_client():
    """Return MongoDB client"""
    try:
        client = MongoClient(Config.MONGODB_URI)
        client.admin.command('ping')
        print("✅ MongoDB connected")
        return client
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

# def get_redis_client():
#     """Return Redis client"""
#     try:
#         client = redis.from_url(Config.REDIS_URL)
#         client.ping()
#         print("✅ Redis connected")
#         return client
#     except Exception as e:
#         print(f"❌ Redis connection failed: {e}")
#         return None
