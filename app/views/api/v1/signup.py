from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository
from app.services.user import UserService

blueprint = Blueprint('signup-api', url_prefix='/signup')


class UserSignupView(HTTPMethodView):
    repository = UserRepository(MySQLConnection)
    service = UserService(repository)

    async def post(self, request: Request):
        await self.service.create(request.json)
        return json({
            'success': True
        })


blueprint.add_route(UserSignupView.as_view(), '/')
