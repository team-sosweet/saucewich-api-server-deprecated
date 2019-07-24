from typing import Dict, Any, List

from pymysql import IntegrityError
from sanic.exceptions import abort

from app.repositories.friend_request import FriendRequestRepository


class FriendRequestService:
    def __init__(self, repository: FriendRequestRepository):
        self.repository = repository

    async def create(self, friend_request: Dict[str, Any]):
        try:
            await self.repository.save(friend_request)
        except IntegrityError:
            abort(409)
        except KeyError:
            abort(400)
        except TypeError:
            abort(400)

    async def get_all(self, recipient: int) -> List[Dict[str, Any]]:
        friend_requests = await self.repository.get_all(recipient)

        return friend_requests

    async def delete(self, seq: int):
        await self.repository.delete(seq)
