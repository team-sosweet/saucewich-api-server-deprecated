from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app import User


class MoneyView(HTTPMethodView):
    async def get(self, request, user_id: int):
        user = await User.get_by_id_or_404(user_id)
        return json({
            'money': user.money
        })

    async def post(self, request: Request, user_id: int):
        user = await User.get_by_id_or_404(user_id)
        user.money += request.json['money']
        await user.save()
        return json({
            'money': user.money
        })
