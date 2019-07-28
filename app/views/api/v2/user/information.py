from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_openapi import doc

from app.misc import models
from app.misc.models import User
from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository
from app.services.user import UserService

blueprint = Blueprint('user-information-api', '/')


class UserInformationView(HTTPMethodView):
    repository = UserRepository(MySQLConnection)
    service = UserService(repository)

    @doc.summary('Get user information')
    @doc.produces(User, description='User of the username', content_type='application/json')
    async def get(self, request, username: str):
        user = await self.service.get(username)
        del user['password']
        return json(user)


blueprint.add_route(UserInformationView.as_view(), '')
