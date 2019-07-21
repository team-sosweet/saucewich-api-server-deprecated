from aiopeewee import model_to_dict
from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from app import User

blueprint = Blueprint(__name__)

class UserResource(HTTPMethodView):
    def get(self, request, user_id: int):
        return json(
            await model_to_dict(User.get(user_id))
        )

blueprint.add_route(UserResource.as_view(), '/user')
