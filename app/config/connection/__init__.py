from .database import DBConnection
from .redis import RedisConnection


db = DBConnection()
redis = RedisConnection()
