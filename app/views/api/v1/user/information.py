from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository
from app.services.user import UserService

blueprint = Blueprint('user-information-api', '/')

class UserInformationView(HTTPMethodView):
    repository = UserRepository(MySQLConnection)
    service = UserService(repository)

    async def get(self, request, username: str):
        user = await self.service.get(username)
        del user['password']
        return json(user)

blueprint.add_route(UserInformationView.as_view(), '/')
