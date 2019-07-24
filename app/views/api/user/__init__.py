from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository
from app.views.api.user.money import UserMoneyView

class UserView(HTTPMethodView):
    repository = UserRepository(MySQLConnection)

    async def get(self, request, username: int):
        user = await self.repository.get(username)
        del user['password']
        return json(user)

blueprint = Blueprint('user-api', '/user/<username>')

blueprint.add_route(UserView.as_view(), '/')
blueprint.add_route(UserMoneyView.as_view(), '/money')
