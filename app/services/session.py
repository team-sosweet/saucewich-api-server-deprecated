import time

from app.repositories.session import SessionRepository


class SessionService:
    def __init__(self, repository: SessionRepository):
        self.repository = repository

    async def add(self, session_id: str):
        await self.repository.set(session_id, {'logged_in_at': time.time()})
        await self.repository.expire(session_id)

    async def exists(self, session_id: str) -> bool:
        await self.repository.expire(session_id)
        return await self.repository.exists(session_id)

    async def remove(self, session_id: str):
        await self.repository.delete(session_id)
