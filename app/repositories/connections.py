from abc import ABC, abstractmethod
from typing import Dict, List, Any

import aiomysql


class DBConnection(ABC):
    @abstractmethod
    @classmethod
    async def initialize(cls, connection_info: Dict[str, Any]):
        ...

    @abstractmethod
    @classmethod
    async def destroy(cls):
        ...

    @abstractmethod
    @classmethod
    async def execute(cls, query, *args) -> int:
        ...

    @abstractmethod
    @classmethod
    async def executemany(cls, query, *args) -> int:
        ...

    @abstractmethod
    @classmethod
    async def fetchall(cls, query, *args) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    @classmethod
    async def fetchone(cls, query, *args) -> Dict[str, Any]:
        ...


class MySQLConnection(DBConnection):
    __pool: aiomysql.Pool = None
    __connection_info = None

    @classmethod
    async def initialize(cls, connection_info: Dict[str, Any]):
        cls.__connection_info = connection_info

    @classmethod
    async def _get_pool(cls) -> aiomysql.Pool:
        if not cls.__pool or cls.__pool.__closed:
            cls.__pool = aiomysql.create_pool(cls.__connection_info)

        return cls.__pool

    @classmethod
    async def execute(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_pool()
        connection: aiomysql.Connection
        cursor: aiomysql.DictCursor

        async with pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                result = cursor.execute(query, *args)

        return result

    @classmethod
    async def executemany(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_pool()
        connection: aiomysql.Connection
        cursor: aiomysql.DictCursor

        async with pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                result = cursor.executemany(query, *args)

        return result

    @classmethod
    async def fetchone(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_pool()
        connection: aiomysql.Connection
        cursor: aiomysql.DictCursor

        async with pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, *args)
                result = await cursor.fetchone(query, *args)

        return result

    @classmethod
    async def fetchall(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_pool()
        connection: aiomysql.Connection
        cursor: aiomysql.DictCursor

        async with pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, *args)
                result = await cursor.fetchall(query, *args)

        return result
