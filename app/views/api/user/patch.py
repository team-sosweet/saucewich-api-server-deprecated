from sanic.exceptions import abort
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository
from app.services.user import UserService


class UserPatchView(HTTPMethodView):
    repository = UserRepository(MySQLConnection)
    service = UserService(repository)

    async def get(self, request, username: str, field_name: str):
        if field_name not in self.repository.patchable_fields:
            abort(404)
        user = await self.service.get(username)
        return json({
            field_name: user[field_name]
        })

    async def post(self, request, username: str, field_name: str):
        if field_name not in self.repository.patchable_fields:
            abort(404)
        user = await self.service.get(username)
        await self.repository.patch(
            username,
            {
                field_name: user[field_name] + request.json[field_name]
            }
        )
        return json({
            'success': True
        })
