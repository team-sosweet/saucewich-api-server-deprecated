from typing import Type, Dict, Any, List, Optional

from app.repositories.connections import DBConnection, KVConnection


class SessionRepository:
    TIMEOUT = 10
    NAMESPACE = 'session'

    def __init__(self, connection: Type[KVConnection]):
        self.connection = connection

    def _make_key_with_namespace(self, key: str) -> str:
        return f'{self.NAMESPACE}:{key}'

    async def exists(self, key: str) -> bool:
        key = self._make_key_with_namespace(key)
        return await self.connection.exists(key)

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        key = self._make_key_with_namespace(key)
        return await self.connection.get(key)

    async def delete(self, key: str):
        key = self._make_key_with_namespace(key)
        await self.connection.delete(key)

    async def set(self, key: str, user_data: Optional[Dict[str, Any]]):
        key = self._make_key_with_namespace(key)
        await self.connection.set(key, user_data)

    async def expire(self, key: str):
        key = self._make_key_with_namespace(key)
        await self.connection.expire(key, self.TIMEOUT)
