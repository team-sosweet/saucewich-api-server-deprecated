from typing import Dict, Any, List

from pymysql import IntegrityError

from app.core.exceptions import UserAlreadyExists, UserNotFound
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, user: Dict[str, Any]):
        try:
            await self.repository.save(user)
        except IntegrityError:
            raise UserAlreadyExists(
                f"""user '{ user['username'] }' already exists"""
            )

    async def patch(self, username: str, patch_data: Dict[str, Any]):
        if not await self.repository.get(username):
            raise UserNotFound(
                f"user '{username}' is not found"
            )

        await self.repository.patch(username, patch_data)

    async def get(self, username: str) -> Dict[str, Any]:
        user = await self.repository.get(username)
        if not user:
            raise UserNotFound(
                f"user '{username}' is not found"
            )

        return user

    async def get_all(self) -> List[Dict[str, Any]]:
        return await self.repository.get_all()
