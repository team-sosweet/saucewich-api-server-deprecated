from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView

from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.views.api.user.money import UserMoneyView
from app.views.api.user.signup import UserSignupView


class UserView(HTTPMethodView):
    repository = UserRepository(MySQLConnection)
    service = UserService(repository)

    async def get(self, request, username: int):
        user = await self.service.get(username)
        del user['password']
        return json(user)

blueprint = Blueprint('user-api', '/user')

blueprint.add_route(UserSignupView.as_view(), '/signup')

blueprint.add_route(UserView.as_view(), '/<username>')
blueprint.add_route(UserMoneyView.as_view(), '/<username>/money')
