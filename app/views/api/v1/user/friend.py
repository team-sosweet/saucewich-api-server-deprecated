from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView

from app.repositories.connections import MySQLConnection
from app.repositories.friend import FriendRepository
from app.repositories.user import UserRepository
from app.services.friend import FriendService
from app.services.user import UserService

blueprint = Blueprint('user-friend-api', url_prefix='/friends')


class UserFriendsView(HTTPMethodView):
    user_repository = UserRepository(MySQLConnection)
    user_service = UserService(user_repository)

    friend_repository = FriendRepository(MySQLConnection)
    friend_service = FriendService(friend_repository)

    async def get(self, request, username: str):
        user = await self.user_service.get(username)
        return json({
            'friends': await self.friend_service.get_all(user['seq'])
        })

    async def post(self, request, username: str):
        user = await self.user_service.get(username)
        if user['seq'] != request.json['user_id']:
            abort(403)

        await self.friend_service.create(request.json)


blueprint.add_route(UserFriendsView.as_view(), '/')
