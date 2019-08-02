from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_openapi import doc
from werkzeug.security import check_password_hash

from app.misc.models import UserAuthentication
from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository
from app.services.user import UserService

blueprint = Blueprint('signin-api', url_prefix='/signin')


class UserSigninView(HTTPMethodView):
    repository = UserRepository(MySQLConnection)
    service = UserService(repository)

    @doc.summary('Authenticate account')
    @doc.consumes(
        UserAuthentication,
        location='body',
        content_type='application/json',
        required=True)
    @doc.produces({'success': bool}, description='the result of account authentication',
                  content_type='application/json')
    async def post(self, request: Request):
        user = await self.service.get(request.json['username'])
        return json({
            'success':
                check_password_hash(user['password'], (request.json['password']))
        })


blueprint.add_route(UserSigninView.as_view(), '/')
