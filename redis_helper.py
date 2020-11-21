import os
import redis


class RedisHelper:
    def __init__(self):
        self.connection = redis.Redis(
            host=os.getenv("REDIS_DB_HOST"),
            port=os.getenv("REDIS_DB_PORT"),
            db=0,
            password=os.getenv("REDIS_DB_PASSWORD"),
            charset="KOI8-R",
            decode_responses=True,
        )
