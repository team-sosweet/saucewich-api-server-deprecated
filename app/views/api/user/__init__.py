from aiopeewee import model_to_dict
from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from app import User
from app.views.api.user.money import MoneyView

class UserView(HTTPMethodView):
    async def get(self, request, user_id: int):
        user = await User.get_or_404(User.id == user_id)
        return json(
            await model_to_dict(user)
        )

blueprint = Blueprint('user-api', '/user/<user_id>')

blueprint.add_route(UserView.as_view(), '/')
blueprint.add_route(MoneyView.as_view(), '/money')
