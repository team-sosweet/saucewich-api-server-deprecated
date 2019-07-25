from typing import List

from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView

from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository
from app.services.user import UserService


def create_patchable_blueprint(field: str) -> Blueprint:
    blueprint = Blueprint(f'user-patch-{field}-api', url_prefix=f'/{field}')

    class UserPatchView(HTTPMethodView):
        repository = UserRepository(MySQLConnection)
        service = UserService(repository)

        field_name: str = field

        async def get(self, request, username: str):
            field_name = self.field_name
            if field_name not in self.repository.patchable_fields:
                abort(404)
            user = await self.service.get(username)
            return json({
                field_name: user[field_name]
            })

        async def post(self, request, username: str):
            field_name = self.field_name
            if field_name not in self.service.patchable_fields:
                abort(403)
            user = await self.service.get(username)
            await self.repository.patch(
                username,
                {
                    field_name: user[field_name] + request.json[field_name]
                }
            )
            return json({
                'success': True
            })

    blueprint.add_route(UserPatchView.as_view(), '/')

    return blueprint


def create_patchable_blueprints() -> List[Blueprint]:
    return list(
        map(create_patchable_blueprint, UserRepository.patchable_fields)
    )
