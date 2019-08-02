from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_openapi import doc

from app.misc.models import FriendRequestCreation, FriendRequest
from app.repositories.connections import MySQLConnection
from app.repositories.friend_request import FriendRequestRepository
from app.repositories.user import UserRepository
from app.services.friend_request import FriendRequestService
from app.services.user import UserService

blueprint = Blueprint('user-friend-request-api', '/requests')


class UserFriendRequestView(HTTPMethodView):
    user_repository = UserRepository(MySQLConnection)
    user_service = UserService(user_repository)

    friend_request_repository = FriendRequestRepository(MySQLConnection)
    friend_request_service = FriendRequestService(friend_request_repository)

    @doc.summary('Get friend requests to the user')
    @doc.produces({'requests': [FriendRequest]}, description='Requests to the user', content_type='application/json')
    async def get(self, request, username: str):
        user = await self.user_service.get(username)
        return json({
            'requests': await self.friend_request_service.get_all(user['seq'])
        })

    @doc.summary('Create friend request')
    @doc.consumes(FriendRequestCreation, location='body', content_type='application/json')
    async def post(self, request, username: str):
        user = await self.user_service.get(username)
        if user['seq'] != request.json['sender']:
            abort(403)

        await self.friend_request_service.create(request.json)


class UserFriendRequestDetailView(HTTPMethodView):
    user_repository = UserRepository(MySQLConnection)
    user_service = UserService(user_repository)

    friend_request_repository = FriendRequestRepository(MySQLConnection)
    friend_request_service = FriendRequestService(friend_request_repository)

    @doc.summary('Get friend request')
    @doc.produces({'request': FriendRequest}, description='Request for the friend_request_id',
                  content_type='application/json')
    async def get(self, request, username: str, friend_request_id: int):
        user = await self.user_service.get(username)
        friend_request = await self.friend_request_service.get(friend_request_id)

        if user['seq'] != friend_request_id['recipient']:
            abort(403)

        return json({
            'request': friend_request
        })

    @doc.summary('Delete the friend request')
    async def delete(self, request, username: str, friend_request_id: int):
        user = await self.user_service.get(username)
        friend_request = await self.friend_request_service.get(friend_request_id)

        if user['seq'] != friend_request['recipient']:
            abort(403)

        await self.friend_request_service.delete(friend_request_id)


blueprint.add_route(UserFriendRequestView.as_view(), '/')
blueprint.add_route(UserFriendRequestDetailView.as_view(), '/<friend_request_id:int>')
