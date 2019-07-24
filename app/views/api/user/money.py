from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository
from app.services.user import UserService


class UserMoneyView(HTTPMethodView):
    repository = UserRepository(MySQLConnection)
    service = UserService(repository)

    async def get(self, request, username: str):
        user = await self.service.get(username)
        return json({
            'money': user['money']
        })

    async def post(self, request: Request, username: str):
        user = await self.service.get(username)
        user['money'] += request.json['money']
        await self.repository.patch(
            username,
            {
                'money': user['money'] + request.json['money']
            }
        )
