import json
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

import aiomysql
import aioredis


class DBConnection(ABC):
    @abstractmethod
    async def initialize(cls, connection_info: Dict[str, Any]):
        ...

    @abstractmethod
    async def destroy(cls):
        ...

    @abstractmethod
    async def execute(cls, query, *args) -> int:
        ...

    @abstractmethod
    async def executemany(cls, query, *args) -> int:
        ...

    @abstractmethod
    async def fetchall(cls, query, *args) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    async def fetchone(cls, query, *args) -> Dict[str, Any]:
        ...


class MySQLConnection(DBConnection):
    __pool: aiomysql.Pool = None
    __connection_info = None

    @classmethod
    async def initialize(cls, connection_info: Dict[str, Any]):
        cls.__connection_info = connection_info

    @classmethod
    async def destroy(cls):
        cls.__pool.close()
        await cls.__pool.wait_closed()

    @classmethod
    async def _get_pool(cls) -> aiomysql.Pool:
        if not cls.__pool or cls.__pool._closed:
            cls.__pool = await aiomysql.create_pool(**cls.__connection_info)

        return cls.__pool

    @classmethod
    async def execute(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_pool()
        connection: aiomysql.Connection
        cursor: aiomysql.DictCursor

        async with pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                result = await cursor.execute(query, *args)

        return result

    @classmethod
    async def executemany(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_pool()
        connection: aiomysql.Connection
        cursor: aiomysql.DictCursor

        async with pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                result = await cursor.executemany(query, *args)

        return result

    @classmethod
    async def fetchone(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_pool()
        connection: aiomysql.Connection
        cursor: aiomysql.DictCursor

        async with pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, *args)
                result = await cursor.fetchone()

        return result

    @classmethod
    async def fetchall(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_pool()
        connection: aiomysql.Connection
        cursor: aiomysql.DictCursor

        async with pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, *args)
                result = await cursor.fetchall()

        return result


class KVConnection(ABC):
    """
    Interface for `key-value database connection`
    """

    @classmethod
    @abstractmethod
    async def initialize(cls, connection_info):
        ...

    @classmethod
    @abstractmethod
    async def destroy(cls):
        ...

    @classmethod
    @abstractmethod
    async def set(cls, key: str, value: Dict[str, Any]) -> None:
        ...

    @classmethod
    @abstractmethod
    async def get(cls, key: str) -> Dict[str, Any]:
        ...

    @classmethod
    @abstractmethod
    async def delete(cls, key: str) -> None:
        ...

    @classmethod
    @abstractmethod
    async def exists(cls, key: str) -> bool:
        ...


class RedisConnection(KVConnection):
    redis: aioredis.Redis = None

    @classmethod
    async def initialize(cls, connection_info: Dict[str, Any]):
        if cls.redis and not cls.redis.closed:
            return cls.redis

        cls.redis = await aioredis.create_redis_pool(**connection_info)

        return cls.redis

    @classmethod
    async def destroy(cls):
        if cls.redis:
            cls.redis.close()
            await cls.redis.wait_closed()

        cls.redis = None

    @classmethod
    async def set(cls, key: str, value: Dict[str, Any]) -> None:
        dumped_value = json.dumps(value)
        await cls.redis.set(key, dumped_value)

    @classmethod
    async def get(cls, key: str) -> Optional[Dict[str, Any]]:
        value = await cls.redis.get(key)
        value = json.loads(value) if value else None

        return value

    @classmethod
    async def delete(cls, key: str) -> None:
        await cls.redis.delete(key)

    @classmethod
    async def exists(cls, key: str) -> bool:
        return cls.redis.exists(key)

    @classmethod
    async def flush_all(cls):
        await cls.redis.flushall()
