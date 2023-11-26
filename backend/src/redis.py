import redis

from src.json import serialize, deserialize


def store_data(redis_client: redis.Redis, key: str, data: dict):
    serialized_data = serialize(data)
    redis_client.set(key, serialized_data)


def get_data(redis_client: redis.Redis, key: str):
    data = redis_client.get(key)
    if data:
        return deserialize(data.decode('utf-8'))
    return None


def delete_key(redis_client: redis.Redis, key: str):
    redis_client.delete(key)
