from aiopeewee import model_to_dict
from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView

from app.models.user import User


blueprint = Blueprint(__name__)

class UserResource(HTTPMethodView):
    async def get(self, request, user_id: int):
        user = await User.get_or_404(User.id == user_id)
        return json(
            await model_to_dict(user)
        )

blueprint.add_route(UserResource.as_view(), '/user/<user_id>')
