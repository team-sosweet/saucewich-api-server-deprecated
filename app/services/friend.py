from typing import Dict, Any, List

from pymysql import IntegrityError
from sanic.exceptions import abort

from app.repositories.friend import FriendRepository


class FriendService:
    def __init__(self, repository: FriendRepository):
        self.repository = repository

    async def create(self, friend: Dict[str, int]):
        try:
            await self.repository.save(friend)
        except IntegrityError:
            abort(409)
        except KeyError:
            abort(400)
        except TypeError:
            abort(400)

    async def get_all(self, user_id: int) -> List[Dict[str, Any]]:
        return await self.repository.get_all(user_id)
