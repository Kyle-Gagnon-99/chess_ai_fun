from src.database import SessionLocal

import redis

# Create a Redis client instance
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def get_redis():
    return redis_client


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
